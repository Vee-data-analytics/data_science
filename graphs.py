import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px

import datetime

import pandas as pd
from dash.dependencies import Output, Input
from django_plotly_dash import DjangoDash

import base64
import datetime
import io

import plotly_express as px
import psycopg2
 
from flask_sqlalchemy import SQLAlchemy

#import sqlalchemy as db
from flask import Flask
 
SQLALCHEMY_TRACK_MODIFICATIONS = True
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'] ,suppress_callback_exceptions=True)


conn = psycopg2.connect(host="localhost",database="zibivaxdb", user="zibivaxuser", password="Movuyi90")
app.server.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://zibivaxuser:Movuyi90@localhost/zibivaxdb"


db = SQLAlchemy(app.server)

class Task(db.Model):
    __tablename__ = 'statboard_tasks'

    allocated_to = db.Column(db.String, nullable=False, primary_key=True)
    work_order_description = db.Column(db.DateTime, nullable=False, primary_key=True)
    status = db.Column(db.String(250), nullable=False, primary_key=True)
    
    def __init__(self, allocated_to, actual_finish_date, status):
        self.Allocated = allocated_to
        self.Finish =  actual_finish_date
        self.Status = status

df = pd.read_sql_table('statboard_tasks', con=db.engine)

app.layout=html.Div([
    html.H1('Stats analysis'),
     dcc.Dropdown(id='employee',
                 options=[{'label':x, 'value':x}
                          for x in sorted(df.allocated_to_id.unique())],
                 value='7',
                 style={'width':'50%'}
                 ),
    dcc.Dropdown(id='Days-worked',
                 options=[{'labels':x, 'value': x}
                           for x in sorted(df.actual_finish_date.unique())],
                 value= datetime,
                 style={'width':'50%'}
    ),


    dcc.Graph(id='stat-graph',
              figure={}),
])
#-----------------------------------------------------------------------------

#fig_pie = px.pie(data_frame=df, name='Genre', values='Japan Sales')
#fig_pie = px.pie(data_frame=df, name='Genre', values='North American Sales')
#fig_pie.show()


#fig_bar = pix.bar(data_frame=df, x='Genre', y='North American Sales')
#fig_bar.show()

#fig_hist = px.histogram(data_frame=df, x='year', y='North American Sales')
#fig_hist.show()


#data interactive graphing with dash 
#-----------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------
@app.callback(Output('postgres_datatable', 'children'),
              [Input('interval_pg', 'n_intervals')])
def populate_datatable(n_intervals):
    df = pd.read_sql_table('statboard_tasks', con=db.engine)
    return [
        dash_table.DataTable(
            id='our-table',
            columns=[{
                         'name': str(x),
                         'id': str(x),
                         'deletable': False,
                     } if x == 'allocated_to_id' or x == 'dispatched_by'
                     else {
                'name': str(x),
                'id': str(x),
                'deletable': True,
            }
                     for x in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_cell={'textAlign': 'left', 'minWidth': '100px', 'width': '100px', 'maxWidth': '100px'},
            style_cell_conditional=[
                {
                    'if': {'column_id': c},
                    'textAlign': 'right'
                } for c in ['allocted_to', 'actual_finish_date']
            ]

        ),
    ]

@app.callback(
    Output(component_id='stat-graph', component_property='figure'),
    [Input(component_id='genre-choice', component_property='value'),
     Input(component_id='platform-choice', component_property='value')]
)

def interactive_graphing(value_genre, value_property='figure'):
    dff = df[df.allocated_to_id==value_genre]
    dff = df[df.actual_finish_date==value_genre]
    fig = px.bar(data_frame=dff, x='allocated_to_id', y='work_order_description')
    


if __name__ == '__main__':
    app.run_server(debug=True)
