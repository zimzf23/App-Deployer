from dependencies import *

@ui.page('/')
def root():
    with ui.header():
        ui.button('Filesystem',on_click=lambda: ui.navigate.to('/fs'))
        ui.button('Source Control',on_click=lambda: ui.navigate.to('/sc'))
        ui.button('Services',on_click=lambda: ui.navigate.to('/sv'))
        ui.button('IIS',on_click=lambda: ui.navigate.to('/sv'))

@ui.page('/fs')
def filesystem():
    ui.label('hello')
    ui.button('Home',on_click=lambda: ui.navigate.to('/'))

ui.run(title='App Deployer', native=True, window_size=(500, 600), fullscreen=False)