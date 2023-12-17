import dash_html_components as html
import os
import pymongo
from murielle import MurielleController

myclient = pymongo.MongoClient(os.environ["MONGODB"])
#from app.components.dating import Dating

mumu = MurielleController()
#récupère la liste des départements pour le menu
departements = mumu.get_departments()
#récupère les indicateurs pour le premier département de la liste
# results = mumu.get_all_indicators_by_department(#retourne une liste de dictionnaires : {"department": indicator_row["department"],"indicatorName": indicator_row["name"], "plot":  plot, "df_cleaned": df_cleaning, "ploting": ploting, "engineering": engineering}
results = mumu.get_all_indicators_by_department(departements[2])
print(results)
#récupère la liste des villes pour le menu
def list_indicator(departements):
    items_liste = [html.Li(indicator) for indicator in departements]
    return html.Ul(items_liste)


layout = (html.Div([
    html.Div(

        children=[

            html.Main(
                className="homepage",
                children=[
                html.H1("Marketing"),
                html.P(children=[
                    list_indicator(departements)]),
                html.Div( children=[
                    str(results[0]["plot"]),
                    ],
                    className="plot"
                )
                ],

                )

        ])
]))
