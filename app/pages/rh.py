import dash
from dash import html, dcc, callback, Input, Output
from murielle import MurielleController
from dash.exceptions import PreventUpdate


# Instance de MurielleController pour récupérer les données
controller = MurielleController()
departments = controller.get_departments()
results = controller.get_all_indicators_by_department("RH")
colors_palette = ['#E1D8F7', '#E4FDE1', '#D7C8F3', '#DAF2D7', '#D0BEF2', '#C6EDC3', '#C0A7EB', '#A7DCA5', '#B596E5', '#90CF8E','#E1D8F7', '#E4FDE1', '#D7C8F3', '#DAF2D7', '#D0BEF2', '#C6EDC3', '#C0A7EB', '#A7DCA5', '#B596E5', '#90CF8E']

def load_indicateur(data):
    for i in data:
        return i


# Fonction pour créer une liste de boutons pour chaque indicateur
def list_indicator(indicators):
    return (html.Div(
        className="div-ul",
        children=
        html.Ul([
            html.Li(indicator['indicatorName'], id=f"indicator-{indicator['indicatorName']}", n_clicks=0)
            for indicator in indicators
        ]),)
    )


# Fonction pour créer un graphique pour chaque indicateur
def plot_indicator(plots):
        return html.Div(
            children=[
                dcc.Graph(
                    figure=plot["plot"].update_layout(paper_bgcolor=colors_palette[i],
                                                      title_font_size=13,
                                                      hovermode='closest',

                                                      ).update_traces(number_font_size=40),
                    id=f"graph-{plot['indicatorName']}",
                    style={"display": "block"},
                    className=plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'])
                for i, plot in enumerate(plots) if plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'] == "indicator"
            ],
            style={"width": "100%"},
            className="indicator-layout"
        )
# def plot_gauge(plots):
#     return html.Div(
#         children=[
#             dcc.Graph(
#                 figure=plot['plot'],
#                 id=f"graph-{plot['indicatorName']}",
#                 style={"display": "block"},
#                 className=plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'])
#             for plot in plots if plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'] == "gauge"
#         ],
#         className="gauge-layout"
#     )
def plot_pie(plots):
    return html.Div(
        children=[
            dcc.Graph(
                figure=plot['plot'],
                id=f"graph-{plot['indicatorName']}",
                style={"display": "block"},
                className=plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'])
            for plot in plots if plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'] == "pie"
        ],
        className="pie-layout"
    )

def plot_other(plots):
    return html.Div(
        children=[
            dcc.Graph(
                figure=plot['plot'],
                id=f"graph-{plot['indicatorName']}",
                style={"display": "block"},
                className=plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'])
            for plot in plots if plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'] != "indicator" and plot["ploting"][load_indicateur(plot["ploting"])]['type_plot'] != "pie"
        ],
        className="graph-layout"
    )


# Layout principal de l'application
layout = (
    html.Aside(
        id="aside",
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
                className="aside-container",
                children=[
                    html.H1(children="Ressources Humaines", className="aside-title"),
                    list_indicator(results),
                ],
            )
        ]
    ),
    html.Div(id='graphs-container', className='graph-layout', children=[
        plot_indicator(results),
        plot_pie(results),
        plot_other(results)
    ]),
    html.Button(
        "<",
        id="toggle-aside-button",
        n_clicks=0,
        className="toggle-aside-button"
    ),
)

# Créer les callbacks pour chaque indicateur
for result in results:
    indicator_name = result['indicatorName']


    @callback(
        Output(f'graph-{indicator_name}', 'style'),
        [Input(f'indicator-{indicator_name}', 'n_clicks')]
    )
    def update_style(click, indicator_name=indicator_name):
        if click is None or click % 2 == 0:
            return {'display': 'block'}
        else:
            return {'display': 'none'}


for result in results:
    indicator_name = result['indicatorName']


    @callback(
        Output(f'indicator-{indicator_name}', 'style'),
        [Input(f'indicator-{indicator_name}', 'n_clicks')]
    )
    def update_style(click, indicator_name=indicator_name):
        if click is None or click % 2 == 0:
            return {'color': 'black'}
        else:
            return {'color': 'rgba(0, 0, 0, .3)', "background-color": "transparent",
                    "border-radius": ".8rem"}


@callback(
    [Output('aside', 'style'),
     Output('toggle-aside-button', 'className')],
    [Input('toggle-aside-button', 'n_clicks')],
)
def toggle_aside(n_clicks):
    if n_clicks is None or n_clicks % 2 == 0:
        # Si le nombre de clics est pair ou None, affiche l'Aside et retire la classe de rotation
        return {'display': 'block'}, 'toggle-aside-button'
    else:
        # Si le nombre de clics est impair, fait disparaître l'Aside et ajoute la classe de rotation
        return {'display': 'none'}, 'toggle-aside-button rotate180'
