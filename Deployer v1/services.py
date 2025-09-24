from dependencies import *
from state import State


def services_body():
    ui.image('/assets/services.png').classes('w-full')
    nssm_env_card()
    nssm_service_card()

@ui.refreshable
def nssm_env_card():

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
    def checkpath_nssm():
        ps_file = Path("Scripts/checkpath_nssm.ps1").resolve()
        subprocess.run([
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command",
            f'Start-Process powershell -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -File "{ps_file}"\' -Verb RunAs'
        ])

    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4 neon-card'):
            ui.label('Nssm Manager').classes('neon-text text-xl font-bold mb-4')
            with ui.row().classes('w-full gap-2 items-stretch'):
                ui.button('Install NSSM', icon='download', on_click=install_nssm).props('color=primary outlined').classes('flex-1 min-w-0')
                ui.button('Check NSSM', icon='check_circle', on_click=checkpath_nssm).props('color=orange outlined').classes('flex-1 min-w-0')
                ui.button('Remove NSSM', icon='delete', on_click=uninstall_nssm).props('color=red outlined').classes('flex-1 min-w-0')

    render()
    return render


@ui.refreshable
def nssm_service_card():

    def create_service_from_state():
        ps_file = Path("Scripts/create-nssm-service.ps1").resolve()

        # wrap each argument as 'arg' and escape inner single quotes -> '' (PowerShell rule)
        def ps_squote(s: str) -> str:
            return "'" + str(s).replace("'", "''") + "'"

        args_list = ", ".join(ps_squote(a) for a in (State.nssm_arguments or []))

        # 1) compose inner argument string (easy to read, no backticks yet)
        inner = (
            f'-NoProfile -ExecutionPolicy Bypass -File "{ps_file}" '
            f'-ServiceName "{State.nssm_service_name}" '
            f'-ExePath "{State.nssm_exe_path}" '
            + (f'-Arguments @({args_list}) ' if args_list else '')
            + (f'-WorkingDir "{State.nssm_working_dir}" ' if State.nssm_working_dir else '')
            + (f'-DisplayName "{State.nssm_display_name}" ' if State.nssm_display_name else '')
            + (f'-Description "{State.nssm_description}" ' if State.nssm_description else '')
            + (f'-LogDir "{State.nssm_log_dir}" ' if State.nssm_log_dir else '')
            + ('-AutoStart ' if State.nssm_auto_start else '')
            + ('-StartNow ' if State.nssm_start_now else '')
            + (f'-RestartDelayMs {int(State.nssm_restart_delay_ms)} ' if State.nssm_restart_delay_ms else '')
            + (f'-ObjectName "{State.nssm_object_name}" ' if State.nssm_object_name else '')
            + (f'-ObjectPassword "{State.nssm_object_password}" '
               if State.nssm_object_name and State.nssm_object_name != "LocalSystem" and State.nssm_object_password else '')
        ).strip()

        # (optional) log & pause in the elevated window
        # log_file = ps_file.with_name(f"{State.nssm_service_name}_create.log")
        # inner += f' *>"{log_file}" ; Read-Host "Done. Press ENTER to close"'

        # 2) escape " as `", then embed in -ArgumentList "..."
        inner_q = inner.replace('"', '`"')
        cmd = f'Start-Process powershell -Verb RunAs -Wait -WindowStyle Normal -ArgumentList "{inner_q}"'

        subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd], check=False)

    @ui.refreshable
    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4 neon-card'):
            ui.label('NSSM Service').classes('neon-text text-xl font-bold mb-4')
            with ui.column().classes('w-full gap-3'):
                ui.input('Service name').props('dense outlined').bind_value(State, 'nssm_service_name').classes('w-full')
                ui.input('Executable path').props('dense outlined').bind_value(State, 'nssm_exe_path').classes('w-full')
                # arguments as a simple space-joined string editor:
                args_input = ui.input('Arguments (space-separated)').props('dense outlined').classes('w-full')
                args_input.value = " ".join(State.nssm_arguments or [])
                args_input.on('change', lambda e: setattr(State, 'nssm_arguments', e.value.split()))
                ui.input('Working dir').props('dense outlined').bind_value(State, 'nssm_working_dir').classes('w-full')
                ui.input('Display name').props('dense outlined').bind_value(State, 'nssm_display_name').classes('w-full')
                ui.input('Description').props('dense outlined').bind_value(State, 'nssm_description').classes('w-full')
                ui.input('Log dir').props('dense outlined').bind_value(State, 'nssm_log_dir').classes('w-full')

                with ui.row().classes('w-full gap-4'):
                    ui.checkbox('Auto start').bind_value(State, 'nssm_auto_start')
                    ui.checkbox('Start now').bind_value(State, 'nssm_start_now')

                ui.number('Restart delay (ms)', format='%d').bind_value(State, 'nssm_restart_delay_ms').classes('w-full')
                ui.input('Run as (ObjectName)').props('dense outlined').bind_value(State, 'nssm_object_name').classes('w-full')
                ui.input('Password').props('dense outlined type=password').bind_value(State, 'nssm_object_password').classes('w-full')

            with ui.row().classes('w-full gap-2 items-stretch mt-2'):
                ui.button('Create / Update Service', icon='play_circle', on_click=create_service_from_state) \
                  .props('color=primary outlined').classes('flex-1 min-w-0')

    render()
    return render