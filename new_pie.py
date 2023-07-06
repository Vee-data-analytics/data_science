import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import sqlalchemy as db
from django_plotly_dash import DjangoDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash('piechart', external_stylesheets=external_stylesheets)

engine = db.create_engine('postgresql+psycopg2://zibivaxuser:Movuyi90@localhost/zibivaxstat')
connection = engine.connect()
metadata = db.MetaData()
statboard = db.Table('statboard_tasks', metadata, autoload=True, autoload_with=engine)

df = pd.read_sql_table('statboard_tasks',connection)

#---------------------------------------------------------------
app.layout = html.Div([
    html.Div([
        html.Label(['Zibivax Staff Data analysis']),
        dcc.Dropdown(
            id='my_dropdown',
            options=[
                 {'name':'id', 'id':'id', 'deletable':False, 'renamable': False},
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
                
            value='task_type',
            multi=False,
            clearable=False,
            style={"width": "50%"}
        ),
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])

#---------------------------------------------------------------
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='my_dropdown', component_property='value')]
)

def update_graph(my_dropdown):
    dff = df

    piechart=px.pie(
            data_frame=dff,
            names=my_dropdown,
            hole=.3,
            )

    return (piechart)
