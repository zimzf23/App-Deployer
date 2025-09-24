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
    def uninstall_nssm():
        bat_file = Path("Scripts/uninstall_nssm.bat").resolve()       
        subprocess.run([
            "powershell", "-Command",
            f'Start-Process "{bat_file}" -Verb RunAs'
        ])

    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4 neon-card'):
            ui.label('Nssm Manager').classes('neon-text text-xl font-bold mb-4')
            with ui.row():
                ui.button('Install NSSM', icon='download', on_click=install_nssm).props('color=primary outlined ').classes('mb-2')
                ui.button('Uninstall NSSM', icon='delete', on_click=install_nssm).props('color=red outlined ').classes('mb-2')
    render()
    return render