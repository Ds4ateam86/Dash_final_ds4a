from turtle import width
import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page
import statsmodels.api as sm
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

register_page(__name__, path="/")

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

fig = px.bar(x=final['Departamento'], y=final['Area'], color=final['Hue'], barmode='group', width=500, height=450)

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
                 width=1200, 
                 height=700)

LEYES_AREA = pd.read_csv('data/DB_AREA_LAWS.csv')

fig2 = make_subplots(specs=[[{"secondary_y": True}]])


fig2.add_trace(
    go.Bar(x= LEYES_AREA['FECHA_year'],y=LEYES_AREA['VAR_AREA'],
    name = "Area of coca"
           
    ))

fig2.add_trace(
    go.Scatter(
        x= LEYES_AREA['FECHA_year'],y=LEYES_AREA['id_ley'], name = "Quantity of laws"
    ),secondary_y=True)

fig2.update_layout(
    title="Quantity of laws VS Areas of Coca",
    legend_title="Graphs",
)


layout=  dbc.Container(
    [
        
       html.Div(children=[
        dcc.Graph(figure=fig, style={'display': 'inline-block', 'margin-right':'15px'}),
        dcc.Graph(figure=fig2, style={'display': 'inline-block', 'width':'500', 'height':'600', 'margin-left':'15px'})
    ]),
       html.Div([
        html.P('With pycaret library, we were able to identify relevant metrics from different models, after analysing the results we decided to use Random Forest Regression. The model predicts the area cultivated in a specific location based on different variables like Base Coca, Municipality, Grid Number, and Total Eradication (manual and aerial). After that, with an extra processing we associated the municipalities with their department to show the sum of cultivated area. '),
        html.P("Exploring the information across time we can see that the quantity of laws and the cultivated area per year in Colombia have a relation between them, may be with 1 or 2 lags (2 years). It means that the Government is taking controls so much slower than the changes in the production of coca. Taking this as an hypothesis, we can compute the granger test to prove the relation."),
        html.P("With a 95% of confidence and the p-value less than 5% we can conclude that there is a time series relation between variables. it means that the impact that the cultivated area of coca has over the quantity of laws is relevant.")
    ]),
       html.Div(children=[
        dcc.Graph(figure=fig1, style={'display': 'inline-block'}),
       ]),
       html.Div([
        html.P("As a measure of the awareness of senators and representatives regarding their knowledge of illicit crops we measure the amount of laws regarding illicit crops. Notice that there is isn't enough laws to determine a strong correlation between the two variables. In fact, we can observe a positive relation between the amount of laws and bills vs the amount of coca cultivated.")
    ])
             
    ]
)  