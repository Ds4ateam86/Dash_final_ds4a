import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import statsmodels.api as sm


register_page(__name__, path="/")

from components.kpi.kpibadge import kpibadge
import plotly.express as px
import pandas as pd
predictions=pd.read_csv('data/modelo.csv')
predictions1=predictions[['Departamento','Coca Cultivation Area']]
predictions2=predictions[['Departamento','Predicted']]
predictions1=predictions1.rename(columns={'Coca Cultivation Area':'Area'})
predictions2=predictions2.rename(columns={'Predicted':'Area'})
predictions1['Hue']='Test'
predictions2['Hue']='Predicted'
final=pd.concat([predictions1,predictions2])
final=final.groupby(['Departamento','Hue'])['Area'].mean()
final=final.reset_index()

fig = px.bar(x=final['Departamento'], y=final['Area'], color=final['Hue'], barmode='group', width=500, height=500)

kpi1 = kpibadge('325', 'Total kpi', 'Danger')
kpi2 = kpibadge('1500', 'Total sales', 'Approved')
kpi3 = kpibadge('325', 'Total transacciones', 'Approved')
kpi4 = kpibadge('2122','Total User', 'Danger')

data_leyes_coca_area = pd.read_csv('data/base_leyes_coca_area.csv')
data_leyes_coca_area['ano'] = data_leyes_coca_area['ano'].astype('str')

fig1 = px.scatter(data_leyes_coca_area, x="Numero de leyes", y="areacoca",
                 size="Erradication_manual", color="ano",
                 size_max=60,
                 trendline='ols',
                 trendline_scope = 'overall',
                 labels={
                     "Numero de leyes":"Number of bills and laws grouped by year",
                     "ano":'Year and trendline',
                     "areacoca":"Coca area cultivated (ha)",
                     "Erradication_manual": "Manual erradication"},
                 title="Number of laws and bills vs Coca area cultivated",
                 width=500, 
                 height=500)


layout=  dbc.Container(
    [
        
       html.Div(children=[
        dcc.Graph(figure=fig, style={'display': 'inline-block'}),
        dcc.Graph(figure=fig1, style={'display': 'inline-block'})
    ])
             
    ]
)  