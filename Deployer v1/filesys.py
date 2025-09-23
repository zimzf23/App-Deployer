from dependencies import *
from state import State

def filesys_body():
    ui.image('/assets/filesystem.png').classes('w-full')
    session_card()


@ui.refreshable
def session_card():
    ROOT = Path('C:/').resolve()

    # ensure attributes exist on the class (safe no-ops if already defined)
    for name in ['app_path', 'backup_path', 'archive_path']:
        if not hasattr(State, name):
            setattr(State, name, '')

    def path_picker_input(label: str, target_attr: str, root: Path = ROOT) -> ui.input:
        """Reusable folder picker input bound to State.<target_attr>"""
        root = root.resolve()

        # bind input directly to State.<target_attr>
        inp = ui.input(label).props('dense outlined').classes('w-full neon-input')
        inp.bind_value(State, target_attr)

        # start from current value if set, else root
        current_str = getattr(State, target_attr, '')
        start_path = Path(current_str) if current_str else root
        picker_state = {'cur': start_path}

        dlg = ui.dialog()
        with dlg:
            with ui.card().classes('min-w-[560px] max-w-[80vw] neon-card'):
                title = ui.label().classes('neon-text')
                with ui.row().classes('gap-2 items-center'):
                    up_btn = ui.button(icon='arrow_upward')
                    refresh_btn = ui.button(icon='refresh')
                    ui.button(icon='done',
                              on_click=lambda: (set_value(picker_state['cur']), dlg.close())
                              ).props('color=primary')
                    ui.space()
                    ui.button(icon='close', on_click=dlg.close).props('flat')
                ui.separator()
                list_box = ui.column().classes('max-h-[50vh] overflow-y-auto w-full')

        def set_value(path: Path):
            # write selection to State.<target_attr>; input updates via binding
            setattr(State, target_attr, str(path))

        def safe_set(path: Path):
            try:
                p = path.resolve()
            except Exception:
                return
            if not str(p).startswith(str(root)):
                return
            picker_state['cur'] = p
            render()

        def list_dirs(path: Path):
            try:
                items = [p for p in path.iterdir() if p.is_dir() and not p.name.startswith('.')]
                return sorted(items, key=lambda x: x.name.lower())
            except PermissionError:
                return []

        def render():
            title.text = f'Current: {picker_state["cur"]}'
            up_btn.on_click(lambda: safe_set(picker_state['cur'].parent if picker_state['cur'] != root else picker_state['cur']))
            refresh_btn.on_click(render)

            for c in list_box.default_slot.children[:]:
                c.delete()

            dirs = list_dirs(picker_state['cur'])
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

        # button inside the input
        with inp.add_slot('append'):
            ui.button('', icon='folder_open', on_click=lambda: (render(), dlg.open())) \
                .props('dense round flat').classes('q-ml-xs')

        return inp

    @ui.refreshable
    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4 neon-card'):
            ui.label('Paths').classes('neon-text text-xl font-bold mb-4')
            with ui.column().classes('w-full gap-3'):
                path_picker_input('Deploy folder',  'app_path',     ROOT)
                path_picker_input('Backup folder',  'backup_path',  ROOT)
                path_picker_input('Archive folder', 'archive_path', ROOT)
            with ui.row().classes('gap-2 mt-4'):
                ui.button('Archive')
                ui.button('Back Up')
                ui.button('Wipe')

    render()
    return render

