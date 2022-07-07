from dash import html 
from PIL import Image

import dash_bootstrap_components as dbc

### Path image edit----------------------------------------------------------------
image_path= 'data/'
#----------------------------------------------------------------------------------


class teambadge:
    def __init__(self,name,label,photo):
        self.photo = photo
        self.name = name
        self.label = label


    def display(self):
        pil_image = Image.open(image_path + self.photo)
        layout = html.Div(
            [
             html.Img(src=pil_image, style={'height':200, 'width':200}),
             html.H2(self.name,className='d-flex justify-content-end' ),
             html.H3(self.label,className='d-flex justify-content-between'),
             
            ], className='m-2'
        )
        return layout

