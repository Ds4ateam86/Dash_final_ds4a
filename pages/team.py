import dash
from dash import html , dcc
import dash_bootstrap_components as dbc
from dash_labs.plugins import register_page

register_page(__name__, path="/team")

from components.kpi.teambadge import teambadge

# Change photo name

kpi1 = teambadge('Emilio Volpe','Mathematician - Data Scientist - Web scraping' , 'emilio.jpeg')
kpi2 = teambadge('Isaac Rodriguez', 'Civil Engineer - BI Analyst - Model designer', 'isaac.jpeg')
kpi3 = teambadge('Jhon Jairo Herrera', 'Electrical Engineer - Front-end developer', 'jhonj.jpeg')
kpi4 = teambadge('Maria Fernanda Ordonez','Statistician - Model designer', 'mafe.jpeg')
kpi5 = teambadge('Paul Rojas', 'Data Analyst - Media editor', 'paul.jpeg')
kpi6 = teambadge('Paula Trejos Silva','Mathematician - Front-end developer', 'paula.jpeg')



layout=  dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                kpi1.display()
            ], className='card')          
        ]),    
        
        dbc.Row([
            dbc.Col([
                kpi2.display()
            ], className='card')          
        ]),
        dbc.Row([
            dbc.Col([
                kpi3.display()
            ], className='card')          
        ]), 
        dbc.Row([
            dbc.Col([
                kpi4.display()
            ], className='card')          
        ]), 
        dbc.Row([
            dbc.Col([
                kpi5.display()
            ], className='card')          
        ]), 
        dbc.Row([
            dbc.Col([
                kpi6.display()
            ], className='card')          
        ]),      
    ]
) 