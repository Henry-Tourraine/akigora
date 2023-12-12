import dash_html_components as html

layout = (
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
