import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import flask
from dash.dependencies import Input, Output

from pages import homepage, direction, rh, marketing, commercial, technique, login

server = flask.Flask(__name__)  # define flask app.server

app = dash.Dash(__name__, server=server, title="Akigora Dashboard",)  # call flask server
app._favicon = "img/muriel_favicon.ico"
# run following in command
# gunicorn graph:app.server -b :8000


df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/' +
    'gdp-life-exp-2007.csv')

app.layout = (
    html.Div(children=[
        dcc.Location(id='url', refresh=False),
        html.Main(id='page-content', className=" layout")
    ]))


@app.callback(Output('url', 'pathname'),
              Input('url', 'pathname'))
def update_pathname(pathname):
    return pathname


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return homepage.layout
    elif pathname == '/direction':
        return direction.layout
    elif pathname == '/ressources-humaines':
        return rh.layout
    elif pathname == '/marketing':
        return marketing.layout
    elif pathname == '/commercial':
        return commercial.layout
    elif pathname == '/technique':
        return technique.layout
    elif pathname == '/login':
       return login.generate_login(app)
    else:
        return '404 - Page not found'


if __name__ == '__main__':
    app.run_server(debug=True)
