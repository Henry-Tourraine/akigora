import dash
from dash import html
from dash import dcc
import pandas as pd
import plotly.graph_objs as go
import flask
from dash.dependencies import Input, Output
from pages import homepage, rh, marketing, commerce, login


server = flask.Flask(__name__)  # define flask app.server

app = dash.Dash(__name__, server=server, title="Akigora Dashboard", suppress_callback_exceptions=True, update_title='Loading...')  # call flask server
app._favicon = "img/muriel_favicon.ico"
# run following in command
# gunicorn graph:app.server -b :8000


app.layout = (
    html.Div(children=[
        dcc.Location(id='url', refresh=False),
        html.Main(id='page-content', className="layout")
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
    elif pathname == '/ressources-humaines':
        return rh.layout
    elif pathname == '/marketing':
        return marketing.layout
    elif pathname == '/commerce':
        return commerce.layout
    elif pathname == '/login':
        return login.layout
    else:
        return '404 - Page not found'


if __name__ == '__main__':
    app.run_server(debug=True)
