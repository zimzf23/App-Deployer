from dependencies import *
from config import load_configuration, save_configuration
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
        with ui.row().classes('w-full gap-2'):
            ui.button(icon='home',on_click=lambda: ui.navigate.to('/'))
            config_buttons()

def source_header():
    with ui.header(elevated=True).style('background-color: grey').classes('items-center justify-between'):
        with ui.row().classes('w-full gap-2'):
            ui.button(icon='home',on_click=lambda: ui.navigate.to('/'))
            config_buttons()

def services_header():
    with ui.header(elevated=True).style('background-color: grey').classes('items-center justify-between'):
        with ui.row().classes('w-full gap-2'):
            ui.button(icon='home',on_click=lambda: ui.navigate.to('/'))
            config_buttons()

def config_buttons():
        ui.button('Load',icon='download',on_click=lambda: load_configuration() ).props('outlined color=primary').classes('flex-1')
        ui.button('Save',icon='save',on_click=lambda: save_configuration()).props('outlined color=primary').classes('flex-1')