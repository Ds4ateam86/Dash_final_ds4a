import dash
from dash_labs.plugins import register_page
import pandas as pd 
import dash_bootstrap_components as dbc
from functools import reduce
register_page(__name__, path="/drugseizure")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

#incautaciones

inca_estupef = pd.read_csv("data/Incautaci_n_de_Estupefacientes.csv", dayfirst=True)
inca_estupef['CANTIDAD'] = inca_estupef['CANTIDAD'].str.replace('.', '')
inca_estupef['CANTIDAD'] = inca_estupef['CANTIDAD'].astype(int)

# adding more variables to dataFrame : AÑO, MES, TONELADAS

inca_estupef['ANNO'] = pd.DatetimeIndex(inca_estupef['FECHA HECHO'], dayfirst= True).year
inca_estupef['MES'] = pd.DatetimeIndex(inca_estupef['FECHA HECHO'], dayfirst=True).month
inca_estupef['TONELADAS'] = (inca_estupef['CANTIDAD'] * 0.001)
df_inc = inca_estupef.groupby(['MES']).sum().reset_index()
anos = inca_estupef['ANNO']
Deptos = inca_estupef['DEPARTAMENTO']
# print(df_inc)
#fig_inc = px.line(df_inc, x="MES", y="TONELADAS", title='Seizures of drugs',  color_discrete_sequence=px.colors.sequential.RdBu)

#--------------------------------------------------------------------------------------------------------
fig3=px.pie(inca_estupef, values="TONELADAS" , names="CLASE BIEN",width=1200, height=400, title="Distribution of drug seizured by type")
fig6=px.histogram(pd.DataFrame(inca_estupef.groupby(['DEPARTAMENTO', 'ANNO'])['TONELADAS'].sum().reset_index()), x="DEPARTAMENTO" , y="TONELADAS",animation_frame="ANNO",width=1200, height=400, title="seizured tons by departments")

layout=  dbc.Container(
    [
        
        dbc.Row([
            dbc.Col([
              html.Div([
                html.Div([
                "FILTRO"
                ]),
                html.Div([
                "AÑO",
                dcc.Dropdown(options=[{'label': x, 'value': x} for x in sorted(anos.unique())], id="years-dropdown", style={'color':'black'}, value = 2010)
            ],style={'display': 'inline-block','margin-left':'15px','width':'40%'}),
              ])  
              
            ]),
            dbc.Col([

                dcc.Graph("pie_graph", style= {'margin-bottom':'50px', 'margin-top': '20px'}),
                dcc.Graph("hist_graph", style= {'margin-top':'50px'}),
            ], xs=12, className='card'),            
        ]),     
    ]
)  
#--------------------------------------------------------------------
# Callbacks----------------------------------------------------------
@callback(
    [Output("pie_graph", "figure"),
    Output("hist_graph", "figure")], 
    Input("years-dropdown", "value")
    )

def figura(input):
    df_filtered = inca_estupef[inca_estupef['ANNO']==input]
    fig3=px.pie(df_filtered, values="TONELADAS" , names="CLASE BIEN",width=1200, height=400, title="Distribution of drug seizured by type")
    fig6=px.histogram(pd.DataFrame(df_filtered.groupby(['DEPARTAMENTO', 'ANNO'])['TONELADAS'].sum().reset_index()), x="DEPARTAMENTO" , y="TONELADAS",animation_frame="ANNO",width=1200, height=400, title="seizured tons by departments")

    return fig3, fig6