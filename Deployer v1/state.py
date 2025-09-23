from dependencies import *

class State:
        current_path = Path('C:/').resolve()
        root_path = ''
        app_path =''
        code_path =''
        backup_path = ''
        archive_path = ''
        repo_url = ''
        repo_branches = [] 
        active_branch = ''

state = State()