import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import sqlalchemy as db
import pandas as pd
import plotly.express as px

app = dash.Dash(__name__)


engine = db.create_engine('postgresql+psycopg2://zibivaxuser:Movuyi90@localhost/zibivaxstat')
connection = engine.connect()
metadata = db.MetaData()
statboard = db.Table('statboard_tasks', metadata, autoload=True, autoload_with=engine)

df = pd.read_sql_table('statboard_tasks',connection)


app.layout = html.Div([
    html.Div([
        dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
        dcc.Input(
            id='adding-rows-name',
            placeholder='Enter a column name...',
            value='',
            style={'padding': 10}
        ),
        html.Button('Add Column', id='adding-columns-button', n_clicks=0)
    ], style={'height': 50}),

    dash_table.DataTable(
        id='our-table',

        columns=[{'name':'id', 'id':'id', 'deletable':False, 'renamable': False},
                 {'name':'code', 'id':'code', 'deletable':False, 'renamable':False},
                 {'name':'work_order_description', 'id': 'work_order_description', 'deletable':False, 'renamable': False},
                 {'name':'task_type', 'id': 'task_type', 'deletable':False, 'renamable': False},
                 {'name':'status', 'id': 'status', 'deletable':False, 'renamable':False},
                 {'name':'allocated_to', 'id': 'allocated_to', 'deletable':False, 'renamable': False},
                 {'name':'dispatched_by', 'id': 'dispatched_by', 'deletable':False, 'renamable': False},
                 {'name':'date_created', 'id': 'date_created', 'deletable':False, 'renamable': False},
                 {'name':'actual_finish_date', 'id': 'actual_finish_date', 'deletable':False, 'renamable': False},
                 {'name':'change_date', 'id': 'change_date', 'deletable':False, 'renamable': False},
                 {'name':'meter_number', 'id': 'meter_number', 'deletable':False, 'renamable':False},
                 {'name':'account_number', 'id': 'account_number', 'deletable':False, 'renamable': False},
                 {'name':'city', 'id': 'city', 'deletable':False, 'renamable': False},
                 {'name':'street_number', 'id': 'street_number', 'deletable':False, 'renamable':False},
                 {'name':'suburb', 'id': 'suburb', 'deletable':False, 'renamable': False},
                 {'name':'unit_no', 'id': 'unit_no', 'deletable':False, 'renamable': False},
                 {'name':'assigned_to_company', 'id': 'assigned_to_company', 'deletable':False, 'renamable': False},
                 {'name':'organisational_unit', 'id': 'organisational_unit', 'deletable':False, 'renamable': False},
                 {'name':'work_order_notes', 'id': 'work_order_notes', 'deletable':False, 'renamable': False}],
                 
        data=df.to_dict('records'),
        editable=True,                  # allow user to edit data inside tabel
        row_deletable=True,             # allow user to delete rows
        sort_action="native",           # give user capability to sort columns
        sort_mode="single",             # sort across 'multi' or 'single' columns
        filter_action="native",         # allow filtering of columns
        page_action='none',             # render all of the data at once. No paging.
        style_table={'height': '300px', 'overflowY': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'right'
            } for c in ['task_type', 'work_order_description']
        ]
    ),

    html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    html.Button('Export to Excel', id='save_to_csv', n_clicks=0),

    # Create notification when saving to excel
    html.Div(id='placeholder', children=[]),
    dcc.Store(id="store", data=0),
    dcc.Interval(id='interval', interval=1000),

    dcc.Graph(id='my_graph')

])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable('our-table')
    ])
# ------------------------------------------------------------------------------------------------

@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



@app.callback(
    Output('our-table', 'columns'),
    [Input('adding-columns-button', 'n_clicks')],
    [State('adding-rows-name', 'value'),
     State('our-table', 'columns')],
)
def add_columns(n_clicks, value, existing_columns):
    print(existing_columns)
    if n_clicks > 0:
        existing_columns.append({
            'name': value, 'id': value,
            'renamable': True, 'deletable': True
        })
    print(existing_columns)
    return existing_columns


@app.callback(
    Output('our-table', 'data'),
    [Input('editing-rows-button', 'n_clicks')],
    [State('our-table', 'data'),
     State('our-table', 'columns')],
)
def add_row(n_clicks, rows, columns):
    # print(rows)
    if n_clicks > 0:
        rows.append({c['id']: '' for c in columns})
    # print(rows)
    return rows


@app.callback(
    Output('my_graph', 'figure'),
    [Input('our-table', 'data')])
def display_graph(data):
    df_fig = pd.DataFrame(data)
    fig = px.bar(df_fig, x='status', y='task_type', color='task_type' )
    return fig


@app.callback(
    [Output('placeholder', 'children'),
     Output("store", "data")],
    [Input('save_to_csv', 'n_clicks'),
     Input("interval", "n_intervals")],
    [State('our-table', 'data'),
     State('store', 'data')]
)
def df_to_csv(n_clicks, n_intervals, dataset, s):
    output = html.Plaintext("The data has been saved to your folder.",
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("", style={'margin': "0px"})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if input_triggered == "save_to_csv":
        s = 6
        df = pd.DataFrame(dataset)
        df.to_csv("Your_Sales_Data.csv")
        return output, s
    elif input_triggered == 'interval' and s > 0:
        s = s-1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s


if __name__ == '__main__':
    app.run_server(debug=True)
