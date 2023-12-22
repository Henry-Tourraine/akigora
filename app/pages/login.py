from dash import html
from dash import dcc
from dash import Input, Output, callback


username = ""
password = ""

layout = (
    html.Div(className="login-form", children=[
        dcc.Link(
            href='/',
            className="logo",
            children=[
                html.Img(
                    className="img-login",
                    src="assets/img/akigora_logo.png",
                    alt="Logo Akigora"
                )]),
        html.Form(children=[
            html.Div(className="label-box", children=[
                dcc.Input(required=True, id="username", value=username),
                html.Label(htmlFor="name", children="Nom d'utilisateur")
            ]),
            html.Div(className="label-box", children=[
                dcc.Input(id="password", required=True, type="password", value=password),
                html.Label(htmlFor="name", children="Mot de passe")
            ]),
            html.Button("Se connecter", className="benjamin"),
        ]),
    ])
)


@callback(
    Output("output", "children"),
    Input("username", "value"),
    Input("password", "value"),
)

def update_output(username, password):
    return print(f'Input 1 {username} and Input 2 {password}')
