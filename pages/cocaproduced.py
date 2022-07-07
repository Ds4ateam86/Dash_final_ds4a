import dash
from dash_labs.plugins import register_page
import pandas as pd 
import dash_bootstrap_components as dbc
from sklearn import preprocessing

register_page(__name__, path="/Cocaproduced")

from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px

BASE_CONSOLIDADA=pd.read_csv("data/Base_consolidada.zip", compression='zip',sep="\t")
## FILL NA

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

ARE_ERR_DEP=BASE_AGRUPADA.groupby(["DEPARTAMENTO","ano"]).agg({'areacoca':'sum', 
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
anos = ARE_ERR_DEP["ano"]
ARE_ERR_DEP.index=ARE_ERR_DEP.DEPARTAMENTO

## VARIABLES STANDARIZATION
ARE_ERR_DEP["Total_seizure_scale"]=preprocessing.scale(ARE_ERR_DEP.Total_seizure)+abs(min(preprocessing.scale(ARE_ERR_DEP.Total_seizure)))
ARE_ERR_DEP["Raw_coca_area_scale"]=preprocessing.scale(ARE_ERR_DEP.Raw_coca_area)+abs(min(preprocessing.scale(ARE_ERR_DEP.Raw_coca_area)))

# map_df = map_df.to_crs(epsg=4326)
# map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
# map_df = map_df.set_index('grilla1')
# map_df = map_df.sample(100)
# join the geodataframe with the cleaned up csv dataframe
#merged = merged.reset_index()

## BARPLOT 
font_color = '#525252'
csfont = {'fontname':'Georgia'} # title font
hfont = {'fontname':'Calibri'} # main font
colors = ['#f47e7a', '#b71f5c', '#621237', '#dbbaa7']

#ax1 = ARE_ERR_DEP[['DEPARTAMENTO','Row_coca_area', 'Total_Eradication']].sort_values(by=['Row_coca_area']).plot.barh(align='center', stacked=True, figsize=(10, 6), color=colors)


#ax2=px.bar(ARE_ERR_DEP[['DEPARTAMENTO','Raw_coca_area_scale', 'Total_seizure_scale']].sort_values(by=['Raw_coca_area_scale']), x=["Raw_coca_area_scale", "Total_seizure_scale"], y="DEPARTAMENTO", title="Raw Coca area Vs Total drugs seazured per Department (Scaled)", orientation='h',  width=1000, height=600)

#plt.title('Row Coca area Vs Total Eradication per Department', fontsize=15, color=font_color, **csfont)
#ax1.set_xlabel("Hectares")
#ax1.set_ylabel("Department")


SEAZ_TYPE=ARE_ERR_DEP.agg({'Base_Cocaine_seizure':'sum',
     'Basuco_seizure':'sum',
     'Cocaine_seizure':'sum',
     'Heroin_seizure':'sum',
     'Dope_seizure':'sum'}).reset_index()
SEAZ_TYPE=pd.DataFrame(SEAZ_TYPE)
SEAZ_TYPE.columns=['Type_seazure', "Quantity"]

#ax3=px.pie(SEAZ_TYPE, values='Quantity', names='Type_seazure', title='Type of drug seizured')

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


                dcc.Graph('drugerr_graph1', style = {'margin-bottom': '20px','margin-top': '20px'}),
                dcc.Graph('drugerr2_graph1', style = {'margin-top': '20px'}),
            ], xs=12, className='card'),
            dbc.Col([
               
                
            ], xs=12, className='card'),             
        ]),     
    ]
)
#--------------------------------------------------------------------
# Callbacks----------------------------------------------------------
@callback(
    [Output("drugerr_graph1", "figure"),
    Output("drugerr2_graph1", "figure")], 
    Input("years-dropdown", "value")
    )

def figura(input):
    df_filtered = ARE_ERR_DEP[ARE_ERR_DEP['ano']==input]
    ax1=px.bar(df_filtered[['DEPARTAMENTO','Raw_coca_area', 'Total_Eradication']].sort_values(by=['Raw_coca_area']), x=["Raw_coca_area", "Total_Eradication"], y="DEPARTAMENTO", title="Raw Coca area Vs Total Eradication per Department", orientation='h',  width=1000, height=600)
    ax2=px.bar(df_filtered[['DEPARTAMENTO','Raw_coca_area_scale', 'Total_seizure_scale']].sort_values(by=['Raw_coca_area_scale']), x=["Raw_coca_area_scale", "Total_seizure_scale"], y="DEPARTAMENTO", title="Raw Coca area Vs Total drugs seazured per Department (Scaled)", orientation='h',  width=1000, height=600)

    return ax1, ax2
