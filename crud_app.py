import base64
import datetime
import io
import dash
from dash import Dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import flask

import pandas as pd
import plotly_express as px
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

server = flask

app = Dash(__name__, server=server, external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] ,suppress_callback_exceptions=True)

#conn = psycopg2.connect(host="localhost",database="zibivaxdb", user="zibivaxuser", password="****")
#app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:'#password'@localhost/statboard_tasks"

db = SQLAlchemy(app.server)

class Task(db.Model):
    __tablename__ = 'statboard_tasks'

    Allocated = db.Columns(db.Integer(250), nullable=False, primary_key=True)
    Finish = db.Columns(db.DateTime[:3], nullable=False, primary_key=True)
    Status = db.Columns(db.String(250), nullable=False, primary_key=True)
    
    def __init__(self, allocated_to, actual_finish_date, status):
        self.Allocated = allocated_to
        self.Finish = actual_finish_date
        self.Status = status

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------


app.layout = html.Div([
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
    # activated once/week or when page refreshed
    dcc.Interval(id='interval_pg', interval=86400000*7, n_intervals=0),
    html.Div(id='output-data-upload'),


    #html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    #html.Button('Export to Excel', id='save_to_csv' , n_clicks=0),
    html.Button('Save to database', id='save_to_postgres', n_clicks=0),

    # notify when saving to excel
    html.Div(id='placeholder', children=[]),
    dcc.Store(id="store", data=0),
    dcc.Interval(id='interval', interval=1000),

    dcc.Graph(id='analysis')
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
        #html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns=[{'name': i, 'id': i} for i in df.columns]
        ),

        html.Hr(),  # horizontal line
    ])
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dash app logic
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d, in
            zip(list_of_contents, list_of_contents, list_of_dates)]
        return children

@app.callback(
    Output('analysis', 'figure'),
    [Input('our-table', 'data')],
    prevent_initial_call=True)
def display_graph(data):
    df_fig = pd.DataFrame(data)
    fig = px.bar(df_fig, x='Price', y='Sales')
    return fig


@app.callback(
    [Output('placeholder', 'children'),
     Output('store', 'data')],
    [Input('save_to_postgres', 'n_clicks'),
     Input('interval', 'n_intervals')],
    [State('output-data-upload', 'data'),
     State('store', 'data')],
    prevent_initial_call=True)
def df_to_postgre(n_clicks, n_intervals, dataset, s):
    df = pd.read_sql_table(table_name= "statboard_tasks", con = db.engine)
    output = html.Plaintext('The data has been saved to your PostgreSQL data table.',
                            style={'color': 'green', 'font-weight': 'bold', 'font-size': 'large'})
    no_output = html.Plaintext("error occured", style={'color':'red', 'font-weight':'bold', 'font-size':'large',})

    input_triggered = dash.callback_context.triggered[0]["prop_id"].split(".")[
        0]

    if input_triggered == "save_to_postgres":
        s = 6
        pg = pd.DataFrame(dataset)
        pg.to_sql('employeelist', con = db.engine, if_exists = 'replace', index = False)
        return output, s
    elif input_triggered == 'interval' and s > 0:
        s = s - 1
        if s > 0:
            return output, s
        else:
            return no_output, s
    elif s == 0:
        return no_output, s



if __name__ == '__main__':
    app.run_server(debug=True)
