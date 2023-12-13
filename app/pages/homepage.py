import dash_html_components as html
import dash_core_components as dcc

layout = (html.Aside(
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
            html.Div(
                className="homepage",
                children=[
                    html.Img(
                        className="logo-homepage",
                        src="assets/img/akigora_logo.png",
                        alt="Logo Akigora"),
                    html.Img(
                        className="img-homepage",
                        src="assets/img/homepage_img.png",
                        alt="Image représentant une femme devant un ordinateur affichant des graphiques")
        ])
)
