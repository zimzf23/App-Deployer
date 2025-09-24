from dependencies import *
from state import State


def services_body():
    ui.image('/assets/services.png').classes('w-full')
    nssm_card()

@ui.refreshable
def nssm_card():

    def install_nssm():
        bat_file = Path("Scripts/install_nssm.bat").resolve()       
        subprocess.run([
            "powershell", "-Command",
            f'Start-Process "{bat_file}" -Verb RunAs'
        ])

    def render():
        with ui.card().classes('neon-card w-full max-w-3xl'):
            ui.button('Install NSSM', icon='download', on_click=install_nssm).props('color=primary outlined').classes('mb-2')
    render()
    return render