import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import flask
from dash.dependencies import Input, Output

from pages import homepage, direction, rh, marketing, commercial, technique

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
    html.Div(className=" layout", children=[
        dcc.Location(id='url', refresh=False),
        html.Aside(
            className="aside",
            children=[
                dcc.Link(
                    href='/',
                    className="logo",
                    children=[
                        html.Img(
                            className="img-aside",
                            src="assets/img/akigora_logo.png",
                            alt="Logo Akigora"
                        )]),
                html.Div(
                    children=[
                        html.H1(children="Départements", className="aside-title"),
                        html.Div(children=[
                            html.P(className="tabs", children=
                                dcc.Link('Direction', href='/direction', id="direction-link", className="link")
                                   ),
                            html.P(children=dcc.Link('Ressources Humaines', href='/ressources-humaines',
                                                     id="ressources-humaines-link", className="link"),
                                   className="tabs"),
                            html.P(children=dcc.Link('Marketing', href='/marketing', id="marketing-link",
                                                     className="link"), className="tabs"),
                            html.P(children=dcc.Link('Commercial', href='/commercial', id="commercial-link",
                                                     className="link"), className="tabs"),
                            html.P(children=dcc.Link('Technique', href='/technique', id="technique-link",
                                                     className="link"), className="tabs")
                        ])
                    ])
            ]
        ),
        html.Main(id='page-content')
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
    else:
        return '404 - Page not found'


# @app.callback()

if __name__ == '__main__':
    app.run_server(debug=True)
