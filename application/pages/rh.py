import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash import dcc

sheet_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=1743150118'
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfProfile = pd.read_csv(csv_export_url)
experts = dfProfile[dfProfile['type'] == 'expert']
expertsWithoutRef = experts[experts['references'].apply(lambda x: pd.isnull(x) or (x == '[]'))]

sheet_indicator_url = "https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=0"
csv_export = sheet_indicator_url.replace('/edit#gid=', '/export?format=csv&gid=')
sheet_indicator = pd.read_csv(csv_export)
indicators = sheet_indicator["Indicateurs"]

labels = ['Expert sans référence', 'Autre']
values = [len(expertsWithoutRef), (len(experts) - len(expertsWithoutRef))]

fig4 = go.Figure(go.Indicator(
    mode="number",
    title={"text": "Nombre d'experts"},
    value=len(experts)),
)
fig1 = go.Figure(go.Pie(labels=labels,
                        values=values))
fig1.update_layout(title="Pourcentage d'entretiens passés")

hourly_price_min_values = dfProfile['daily_hourly_prices.hourly_price_min'].dropna()
hourly_price_max_values = dfProfile['daily_hourly_prices.hourly_price_max'].dropna()
df_expert = dfProfile[dfProfile['type'] == 'expert']
taux_journalier_max = round(df_expert['daily_hourly_prices.daily_price_max'].mean())
taux_journalier_min = round(df_expert['daily_hourly_prices.hourly_price_min'].mean())
taux_horaire_moyen = round(((hourly_price_min_values + hourly_price_max_values) / 2).mean())

fig2 = go.Figure(go.Indicator(
    mode="number",
    value=taux_journalier_max,
    title="Taux journalier maximum (en €)",
    number={'valueformat': ',',
            }))

hourly_price_min_values = dfProfile['daily_hourly_prices.hourly_price_min'].dropna()
hourly_price_max_values = dfProfile['daily_hourly_prices.hourly_price_max'].dropna()

taux_journalier_max = round(df_expert['daily_hourly_prices.hourly_price_max'].mean())
taux_journalier_min = round(df_expert['daily_hourly_prices.hourly_price_min'].mean())
taux_horaire_moyen = round(((hourly_price_min_values + hourly_price_max_values) / 2).mean())

fig3 = go.Figure()

fig3.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=taux_horaire_moyen,
    title={'text': "Taux Horaire Moyen",
           'font': {'size': 20}},
    gauge={'axis': {'range': [taux_journalier_min, taux_journalier_max]},
           'bar': {'color': "gold"},  # Set the color to gold
           }))


def list_indicator(indicators):
    items_liste = [html.Li(indicator) for indicator in indicators]
    return html.Ul(items_liste)


layout = (
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
                className="aside-container",
                children=[
                    html.H1(children="Ressources Humaines", className="aside-title"),
                    html.Div(children=[
                        list_indicator(indicators)
                    ])
                ])
        ]
    ),
    html.Div(className='graph-layout', children=[
        dcc.Graph(figure=fig2, className="pie-chart"),
        dcc.Graph(figure=fig1, className="pie-chart"),
        dcc.Graph(figure=fig3, className="pie-chart"),
        dcc.Graph(figure=fig4, className="pie-chart")
    ]))
