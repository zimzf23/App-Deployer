
from dependencies import *

def styles():
    ui.colors(blight='#71a8da')
    ui.add_head_html('<style>body {background-color: GhostWhite; }</style>')
    ui.add_css('''
    @font-face{
        font-family: "Magistral";
        src: url('assets/Magistral-Medium.ttf') format('truetype');
    }
    @font-face{
        font-family: "Muli";
        src: url('assets/Muli-Regular.ttf') format('truetype');
    }
    @font-face{
        font-family: "Muli-SB";
        src: url('assets/Muli-SemiBold.ttf') format('truetype');
    }
    ''')

def basic_header():
    with ui.header(elevated=True).style('background-color: white').classes('items-center justify-between'):
        ui.button('Home',on_click=lambda: ui.navigate.to('/'))
        ui.button('Filesystem',on_click=lambda: ui.navigate.to('/fs'))
        ui.button('Source Control',on_click=lambda: ui.navigate.to('/sc'))
        ui.button('Services',on_click=lambda: ui.navigate.to('/sv'))
        ui.button('IIS',on_click=lambda: ui.navigate.to('/sv'))

