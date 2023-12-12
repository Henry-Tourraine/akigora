import pandas as pd
import plotly.graph_objs as go
from dash import dcc
import dash_html_components as html

sheet_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=1743150118'
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfProfile = pd.read_csv(csv_export_url)
experts = dfProfile[dfProfile['type'] == 'expert']
expertsWithoutRef = experts[experts['references'].apply(lambda x: pd.isnull(x) or (x == '[]'))]

newsletter_url = 'https://docs.google.com/spreadsheets/d/1dgytVKilFnayj8sdFkyHaDzXPBD3bNHIBoCOzJY8SWE/edit#gid=963445449'
csv_export_url = newsletter_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfNewletter = pd.read_csv(csv_export_url)

user_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=2104663239'
csv_export_url = user_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfUser = pd.read_csv(csv_export_url)

profile_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=1743150118'
csv_export_url = profile_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfProfile = pd.read_csv(csv_export_url)

company_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=50343459'
csv_export_url = company_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfCompany = pd.read_csv(csv_export_url)

intervention_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=1957285512'
csv_export_url = intervention_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfIntervention = pd.read_csv(csv_export_url)

recommandation_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=1084005917'
csv_export_url = recommandation_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfRecommandation = pd.read_csv(csv_export_url)

search_url = 'https://docs.google.com/spreadsheets/d/1OeVY-kCiQAd_TMKmANBRyqsUKvNZV1w1/edit#gid=907797096'
csv_export_url = search_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfSearch = pd.read_csv(csv_export_url)

consultation_url = 'https://docs.google.com/spreadsheets/d/11R_8DVW0rogGz8YYNMEN-KcsqvQVNAVzFQX4FmruadY/edit#gid=1396684367'
csv_export_url = consultation_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfConsultation = pd.read_csv(csv_export_url)


labels = ['Expert sans référence', 'Autre']
values = [len(expertsWithoutRef), (len(experts) - len(expertsWithoutRef))]

fig = go.Figure(go.Pie(labels=labels,
                       values=values))

fig.update_layout(title='d\'entretiens passés')



hourly_price_min_values = dfProfile['daily_hourly_prices.hourly_price_min'].dropna()
hourly_price_max_values = dfProfile['daily_hourly_prices.hourly_price_max'].dropna()
df_expert = dfProfile[dfProfile['type'] == 'expert']
taux_journalier_max = round(df_expert['daily_hourly_prices.daily_price_max'].mean())
taux_journalier_max = round(df_expert['daily_hourly_prices.hourly_price_max'].mean())
taux_journalier_min = round(df_expert['daily_hourly_prices.hourly_price_min'].mean())
taux_horaire_moyen = round(((hourly_price_min_values + hourly_price_max_values) / 2).mean())

fig2 = go.Figure(go.Indicator(
        mode="number",
        value=taux_journalier_max,
        title="Taux journalier maximum (en €)",
        number={'valueformat': ',',
                'font': {'size': 140}}))

layout = html.Div(className='graph-layout', children=[
    dcc.Graph(figure=go.Figure(go.Indicator(
        mode="number",
        title={"text": "Nombre d'experts"},
        value=len(experts))
    )
        , className="number-indicator", animate=True),
    dcc.Graph(figure=fig, className="pie-chart"),
    dcc.Graph(figure=go.Figure(go.Indicator(
        mode="number",
        title={"text": "Nombre d'experts"},
        value=len(experts))
    ),
        className="number-indicator", animate=True),
    dcc.Graph(figure=fig, className="pie-chart"),
    dcc.Graph(figure=fig2)

])
