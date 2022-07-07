from turtle import left
import dash
from dash_labs.plugins import register_page
import pandas as pd 
import dash_bootstrap_components as dbc
from functools import reduce
register_page(__name__, path="/drugeradication")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

BASE_CONSOLIDADA=pd.read_csv("data/Base_consolidada.zip", compression='zip',sep="\t")

BASE_CONSOLIDADA.Erradication_manual=BASE_CONSOLIDADA.Erradication_manual.fillna(0)
BASE_CONSOLIDADA.Erradication_aerea=BASE_CONSOLIDADA.Erradication_aerea.fillna(0)
BASE_CONSOLIDADA.BASE_COCA_incaut=BASE_CONSOLIDADA.BASE_COCA_incaut.fillna(0)
BASE_CONSOLIDADA.BASUCO_incaut=BASE_CONSOLIDADA.BASUCO_incaut.fillna(0)
BASE_CONSOLIDADA.COCAINA_incaut=BASE_CONSOLIDADA.COCAINA_incaut.fillna(0)
BASE_CONSOLIDADA.HEROINA_incaut=BASE_CONSOLIDADA.HEROINA_incaut.fillna(0)
BASE_CONSOLIDADA.MARIHUANA_incaut=BASE_CONSOLIDADA.MARIHUANA_incaut.fillna(0)


## NEW VARIABLES

BASE_CONSOLIDADA['Total_Erradicacion']=BASE_CONSOLIDADA.Erradication_manual+BASE_CONSOLIDADA.Erradication_aerea
BASE_CONSOLIDADA['Total_Incautados']=BASE_CONSOLIDADA.BASE_COCA_incaut+BASE_CONSOLIDADA.BASUCO_incaut+BASE_CONSOLIDADA.COCAINA_incaut+BASE_CONSOLIDADA.HEROINA_incaut+BASE_CONSOLIDADA.MARIHUANA_incaut

## FIRST AGRUPATION DATA BASE
BASE_AGRUPADA=BASE_CONSOLIDADA.groupby(['DEPARTAMENTO', 'MPIO_CNMBR', 'ano', 'MPIO_CCNCT']).agg({'areacoca':'sum', 
                                                                                            'Total_Erradicacion':'max', 
                                                                                            'Erradication_manual':'max',
                                                                                            'Erradication_aerea':'max',
                                                                                            'BASE_COCA_incaut':'max',
                                                                                            'BASUCO_incaut':'max',
                                                                                            'COCAINA_incaut':'max',
                                                                                            'HEROINA_incaut':'max',
                                                                                            'MARIHUANA_incaut':'max',
                                                                                            'Total_Incautados':'max'}).reset_index()

## SECOND AGRUPATION DATA BASE

ARE_ERR_DEP=BASE_AGRUPADA.groupby(["DEPARTAMENTO",'ano']).agg({'areacoca':'sum', 
                                                     'Total_Erradicacion':'sum', 
                                                     'Erradication_manual':'sum',
                                                     'Erradication_aerea':'sum',
                                                     'BASE_COCA_incaut':'sum',
                                                     'BASUCO_incaut':'sum',
                                                     'COCAINA_incaut':'sum',
                                                     'HEROINA_incaut':'sum',
                                                     'MARIHUANA_incaut':'sum',
                                                     'Total_Incautados':'sum'}).reset_index()
### RENAME VARIABLES
ARE_ERR_DEP.rename(columns={"areacoca":'Raw_coca_area', 
                            "Total_Erradicacion":'Total_Eradication', 
                            "Erradication_manual":'Manual_Eradication', 
                            "Erradication_aerea":'Aerial_Eradication',
                            "BASE_COCA_incaut":"Base_Cocaine_seizure",
                            "BASUCO_incaut":"Basuco_seizure",
                            "COCAINA_incaut":"Cocaine_seizure",
                            "HEROINA_incaut":"Heroin_seizure",
                            "MARIHUANA_incaut":"Dope_seizure",
                            "Total_Incautados":"Total_seizure"}, inplace = True)
Deptos = ARE_ERR_DEP['DEPARTAMENTO']
anos = ARE_ERR_DEP['ano']
ARE_ERR_DEP.index=ARE_ERR_DEP.DEPARTAMENTO

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
                dcc.Dropdown(options=[{'label': x, 'value': x} for x in sorted(anos.unique())], id="years-dropdown", style={'color':'black'}, value = 2001)
            ],style={'display': 'inline-block','margin-left':'15px','width':'40%'}),
              ])  
              
            ]),
            dbc.Col([
                dcc.Graph("cocaprodair_graph1", style = {'margin-bottom': '20px', 'margin-top': '20px'}),
                dcc.Graph("cocaprodhand_graph1", style = {'margin-top': '20px'}),
            ], xs=12, className='card'),            
        ]),     
    ]
)  

@callback(
    [Output("cocaprodair_graph1", "figure"),
    Output("cocaprodhand_graph1", "figure")], 
    Input("years-dropdown", "value")
    )

def figura(input):
    df_filtered = ARE_ERR_DEP[ARE_ERR_DEP['ano']==input]
    
    fig4=px.bar(df_filtered, x="DEPARTAMENTO" , y="Aerial_Eradication", width=1200, height=400,title="Tons of Cocaine eradicated by air")
    fig5=px.bar(df_filtered, x="DEPARTAMENTO" , y="Manual_Eradication", width=1200, height=400,title="Tons of Cocaine eradicated by hand")

    return fig4, fig5