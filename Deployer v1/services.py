from dependencies import *
from state import State


def services_body():
    ui.image('/assets/services.png').classes('w-full')
    nssm_card()

@ui.refreshable
def nssm_card():

    def install_nssm():
        ps_file = Path("Scripts/install_nssm.ps1").resolve()
        subprocess.run([
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
            f'Start-Process powershell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -File "{ps_file}"\' -Verb RunAs'
        ])
    def uninstall_nssm():
        ps_file = Path("Scripts/uninstall_nssm.ps1").resolve()
        subprocess.run([
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
            f'Start-Process powershell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -File "{ps_file}"\' -Verb RunAs'
        ])

    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4 neon-card'):
            ui.label('Nssm Manager').classes('neon-text text-xl font-bold mb-4')
            with ui.row():
                ui.button('Install NSSM', icon='download', on_click=install_nssm).props('color=primary outlined ').classes('mb-2')
                ui.button('Uninstall NSSM', icon='delete', on_click=uninstall_nssm).props('color=red outlined ').classes('mb-2')
    render()
    return render