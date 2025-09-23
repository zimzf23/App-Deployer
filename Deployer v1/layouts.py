from dependencies import *

def styles():
    ui.colors(primary='green', secondary='orange',dark_page='#000000', )
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

def filesys_header():
    with ui.header(elevated=True).style('background-color: grey').classes('items-center justify-between'):
        ui.button(icon='home',on_click=lambda: ui.navigate.to('/'))
def source_header():
    with ui.header(elevated=True).style('background-color: grey').classes('items-center justify-between'):
        ui.button(icon='home',on_click=lambda: ui.navigate.to('/'))

