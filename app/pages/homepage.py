from dash import html
from dash import dcc

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
                html.Div(
                    className="tabs-container",
                    children=[
                        dcc.Link('Ressources Humaines', href='/ressources-humaines',
                                 id="ressources-humaines-link", className="tabs link"),
                        dcc.Link('Marketing', href='/marketing', id="marketing-link",
                                 className="tabs link"),
                        dcc.Link('Commerce', href='/commercial', id="commercial-link",
                                 className="tabs link"),
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
