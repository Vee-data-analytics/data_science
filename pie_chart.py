import plotly.express as px
import pandas as pd
import psycopg2

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as db
import dash

conn = psycopg2.connect(host="localhost",
                        database="zibivaxdb",
                        user="zibivaxuser",
                        password="Movuyi90")
 


app = dash.Dash(__name__, external_stylesheets='external_stylesheets')
server = app.server

engine = db.create_engine('postgresql+psycopg2://zibivaxuser:Movuyi90@localhost/zibivaxdb')
connection = engine.connect()
metadata = db.MetaData()
statboard = db.Table('statboard_tasks', metadata, autoload=True, autoload_with=engine)

df = pd.read_sql_table('statboard_tasks',connection)


#--------------------------------------------------------------

# Store the columes in seperate variable


def my_down(my_dropdown):
    values = df['status']
    names = df['work_order_description']
    
    # Create the pie chart
    
    performed_graph = px.pie(df, values=values, names=names, title='Video game sales')
    
    # Update traces
    performed_graph.update_traces(
        textposition='inside',
        textinfo='label'
    )
    return (performed_graph)


if __name__ == '__main__':
    app.run_server(debug=True)