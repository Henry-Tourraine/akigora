import dash
import dash_core_components as dcc
import dash_html_components as html

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Basic Dash App'),

    html.Div(children='''
        A simple example of a Dash web application.
    '''),

    # Create a scatter plot using Dash Core Components
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'scatter', 'name': 'Trace 1'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'scatter', 'name': 'Trace 2'},
            ],
            'layout': {
                'title': 'Scatter Plot Example'
            }
        }
    )
])

def app():
    app.run_server(debug=True)