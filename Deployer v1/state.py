from dependencies import *

class State:
    def __init__(self):
        self.current_path = Path('C:/').resolve()
        self.app_path = ''

state = State()