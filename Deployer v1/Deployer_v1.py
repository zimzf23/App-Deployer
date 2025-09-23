from dependencies import *
from layouts import basic_header, styles

@ui.page('/')
def root():
    styles()

@ui.page('/fs')
def filesystem():
    basic_header()


ui.run(title='App Deployer', native=True, window_size=(500, 600), fullscreen=False)