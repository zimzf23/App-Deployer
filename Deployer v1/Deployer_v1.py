from dependencies import *
from filesys import filesys_body
from source import source_body
from layouts import source_header, filesys_header, services_header, styles
from services import services_body
@ui.page('/')
def root():
    styles()
    
    with ui.column().classes('w-full h-full items-center justify-center gap-4'):
        ui.image('/assets/banner.png').classes('w-full')
        button_style = 'width:200px'  # adjust width as needed
        bttnprops = 'outline color=green '
        ui.button('Filesystem',on_click=lambda: ui.navigate.to('/fs')).style(button_style).props(bttnprops)
        ui.button('Source Control',on_click=lambda: ui.navigate.to('/sc')).style(button_style).props(bttnprops)
        ui.button('Services',on_click=lambda: ui.navigate.to('/sv')).style(button_style).props(bttnprops)
        ui.button('IIS',on_click=lambda: ui.navigate.to('/sv')).style(button_style).props(bttnprops)

@ui.page('/fs')
def filesystem():
    styles()
    filesys_header()
    filesys_body()

@ui.page('/sc')
def filesystem():
    styles()
    source_header()
    source_body()   

@ui.page('/sv')
def filesystem():
    styles()
    services_header()
    services_body()  


ui.run(title='App Deployer', native=True, window_size=(600, 800), fullscreen=False, dark=True, uvicorn_reload_excludes='env/*')