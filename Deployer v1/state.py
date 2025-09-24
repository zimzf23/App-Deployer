from dependencies import *

class State:
    current_path = Path('C:/').resolve()
    root_path = ''
    app_path = ''
    code_path = ''
    backup_path = ''
    archive_path = ''
    repo_url = ''
    repo_branches = []
    active_branch = ''

    # --- NSSM service config (PERSISTED TO TOML) ---
    nssm_service_name = 'MyAppSvc'
    nssm_exe_path = r'C:\Python313\python.exe'
    nssm_arguments = [r'C:\apps\myapp\main.py']
    nssm_working_dir = r'C:\apps\myapp'
    nssm_display_name = 'My App Service'
    nssm_description = 'Managed by NSSM'
    nssm_log_dir = r'C:\nssm\logs'
    nssm_auto_start = True
    nssm_start_now = True
    nssm_restart_delay_ms = 5000
    nssm_object_name = 'LocalSystem'          # or 'DOMAIN\\user'
    nssm_object_password = ''                 # <-- WILL be saved to TOML

