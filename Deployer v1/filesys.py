from dependencies import *

def filesys_body():
    ui.image('/assets/filesystem.png').classes('w-full')
    session_card()


@ui.refreshable
def session_card():
    # Root restricted to C: drive
    ROOT = Path('C:/').resolve()

    def path_picker_input(label: str = 'Path', root: Path = ROOT) -> ui.input:
        root = root.resolve()
        inp = ui.input(label).props('dense outlined').classes('w-full')
        state = {'cur': root}

        dlg = ui.dialog()
        with dlg:
            with ui.card().classes('min-w-[560px] max-w-[80vw]'):
                title = ui.label()
                with ui.row().classes('gap-2 items-center'):
                    up_btn = ui.button(icon='arrow_upward')        # up
                    new_btn = ui.button(icon='create_new_folder')  # new folder
                    refresh_btn = ui.button(icon='refresh')        # refresh
                    ui.button(icon='done',
                              on_click=lambda: (set_value(state['cur']), dlg.close())
                              ).props('color=primary')
                    ui.space()
                    ui.button(icon='close', on_click=dlg.close).props('flat')
                ui.separator()
                list_box = ui.column().classes('max-h-[50vh] overflow-y-auto w-full')

        def set_value(path: Path):
            inp.value = str(path)

        def safe_set(path: Path):
            try:
                p = path.resolve()
            except Exception:
                return
            if not str(p).startswith(str(root)):
                return
            state['cur'] = p
            render()

        def list_dirs(path: Path):
            try:
                items = [p for p in path.iterdir() if p.is_dir() and not p.name.startswith('.')]
                return sorted(items, key=lambda x: x.name.lower())
            except PermissionError:
                return []

        def new_folder():
            nd = ui.dialog()
            with nd:
                with ui.card().classes('min-w-[420px]'):
                    ui.label(f'Create in:\n{state["cur"]}').classes('text-sm opacity-75')
                    name_input = ui.input('Folder name').props('outlined dense').classes('w-full mt-2')
                    with ui.row().classes('justify-end gap-2 mt-2'):
                        ui.button(icon='close', on_click=nd.close).props('flat')
                        def do_create():
                            name = (name_input.value or '').strip()
                            if not name:
                                ui.notify('Please enter a folder name', color='warning'); return
                            if any(c in '<>:"/\\|?*' for c in name):
                                ui.notify('Illegal characters: <>:"/\\|?*', color='negative'); return
                            target = (state['cur'] / name)
                            if not str(target.resolve()).startswith(str(root)):
                                ui.notify('Path outside allowed root', color='negative'); return
                            if target.exists():
                                ui.notify('Folder already exists', color='warning'); return
                            try:
                                target.mkdir()
                                ui.notify(f'Created: {target}')
                                nd.close()
                                render()
                            except PermissionError:
                                ui.notify('Permission denied', color='negative')
                            except OSError as e:
                                ui.notify(f'Error: {e}', color='negative')
                        ui.button(icon='done', on_click=do_create).props('color=primary')
            nd.open()

        def render():
            title.text = f'Current: {state["cur"]}'
            up_btn.on_click(lambda: safe_set(state['cur'].parent if state['cur'] != root else state['cur']))
            refresh_btn.on_click(render)
            new_btn.on_click(new_folder)

            for c in list_box.default_slot.children[:]:
                c.delete()

            dirs = list_dirs(state['cur'])
            with list_box:
                if not dirs:
                    ui.label('(no subfolders or permission denied)').classes('opacity-70')
                else:
                    for d in dirs:
                        with ui.row().classes('w-full items-center justify-between py-1'):
                            ui.label(d.name)
                            with ui.row().classes('gap-2'):
                                ui.button(icon='folder_open', on_click=lambda d=d: safe_set(d)).props('dense')
                                ui.button(icon='done', on_click=lambda d=d: (safe_set(d), set_value(d), dlg.close())).props('flat dense')

        # input button (folder icon)
        with inp.add_slot('append'):
            ui.button('', icon='folder_open', on_click=lambda: (render(), dlg.open())) \
                .props('dense round flat') \
                .classes('q-ml-xs')

        return inp

    @ui.refreshable
    def render():
        with ui.card().classes('w-full max-w-2xl mx-auto p-4'):
            with ui.column().classes('w-full gap-3'):
                ui.label('App Path:')
                path_picker_input('Deploy folder', ROOT)
    render()
    return render

