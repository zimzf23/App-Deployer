from dependencies import *
from state import State

def filesys_body():
    ui.image('/assets/filesystem.png').classes('w-full')
    session_card()


@ui.refreshable
def session_card():
    ROOT = Path('C:/').resolve()

    def path_picker_input(label: str = 'Path', root: Path = ROOT) -> ui.input:
        root = root.resolve()

        # bind input to State.app_path
        inp = ui.input(label).props('dense outlined').classes('w-full neon-input')
        inp.bind_value(State, 'app_path')

        picker_State = {'cur': Path(State.app_path) if State.app_path else root}

        dlg = ui.dialog()
        with dlg:
            with ui.card().classes('min-w-[560px] max-w-[80vw] neon-card'):
                title = ui.label().classes('neon-text')
                with ui.row().classes('gap-2 items-center'):
                    up_btn = ui.button(icon='arrow_upward')
                    refresh_btn = ui.button(icon='refresh')
                    ui.button(icon='done',
                              on_click=lambda: (set_value(picker_State['cur']), dlg.close())
                              ).props('color=primary')
                    ui.space()
                    ui.button(icon='close', on_click=dlg.close).props('flat')
                ui.separator()
                list_box = ui.column().classes('max-h-[50vh] overflow-y-auto w-full')

        def set_value(path: Path):
            State.app_path = str(path)   # updates both State + bound input

        def safe_set(path: Path):
            try:
                p = path.resolve()
            except Exception:
                return
            if not str(p).startswith(str(root)):
                return
            picker_State['cur'] = p
            render()

        def list_dirs(path: Path):
            try:
                items = [p for p in path.iterdir() if p.is_dir() and not p.name.startswith('.')]
                return sorted(items, key=lambda x: x.name.lower())
            except PermissionError:
                return []

        def render():
            title.text = f'Current: {picker_State["cur"]}'
            up_btn.on_click(lambda: safe_set(picker_State['cur'].parent if picker_State['cur'] != root else picker_State['cur']))
            refresh_btn.on_click(render)

            for c in list_box.default_slot.children[:]:
                c.delete()

            dirs = list_dirs(picker_State['cur'])
            with list_box:
                if not dirs:
                    ui.label('(no subfolders or permission denied)').classes('opacity-70')
                else:
                    for d in dirs:
                        with ui.row().classes('w-full items-center justify-between py-1'):
                            ui.label(d.name).classes('neon-text')
                            with ui.row().classes('gap-2'):
                                ui.button(icon='folder_open', on_click=lambda d=d: safe_set(d)).props('dense')
                                ui.button(icon='done', on_click=lambda d=d: (safe_set(d), set_value(d), dlg.close())).props('flat dense')

        with inp.add_slot('append'):
            ui.button('', icon='folder_open', on_click=lambda: (render(), dlg.open())) \
                .props('dense round flat').classes('q-ml-xs')

        return inp

    @ui.refreshable
    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4 neon-card'):
            ui.label('App path').classes('neon-text text-xl font-bold mb-4')
            with ui.column().classes('w-full gap-3'):
                path_picker_input('Deploy folder', ROOT)
                path_picker_input('Backup folder', ROOT)
                path_picker_input('Archive folder', ROOT)
            with ui.row():
                ui.button('Archive')
                ui.button('Back Up')
                ui.button('Wipe')

    render()
    return render

