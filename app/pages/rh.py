import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash import dcc

sheet_url = 'https://docs.google.com/spreadsheets/d/1Fx_SjWbTV0J2jvtXrWdkQsLS5-9AazAt7nrywB2sy4w/edit#gid=1743150118'
csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
dfProfile = pd.read_csv(csv_export_url)
experts = dfProfile[dfProfile['type'] == 'expert']


fig = go.Figure(go.Indicator(
    mode="number",
    title={"text": "Nombre d'experts"},
    value=len(experts))
)

layout = (
    dcc.Graph(figure=fig, className="number-indicator", animate=True)
)
