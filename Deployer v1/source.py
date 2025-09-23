from dependencies import *
from state import State

def source_body():
    ui.image('/assets/source.png').classes('w-full')
    gitpath_card()


@ui.refreshable
def gitpath_card():

    def _parse_repo_identifier(s: str) -> str | None:
        """Accept full GitHub URL or owner/repo; return 'owner/repo' or None."""
        if not s:
            return None
        s = s.strip()
        if 'github.com' in s:
            parts = s.split('github.com/', 1)[-1].split('/')
            if len(parts) >= 2 and parts[0] and parts[1]:
                return f"{parts[0]}/{parts[1].removesuffix('.git')}"
            return None
        if '/' in s and len(s.split('/')) == 2:
            owner, repo = s.split('/', 1)
            owner, repo = owner.strip(), repo.strip().removesuffix('.git')
            if owner and repo:
                return f'{owner}/{repo}'
        return None

    # --- PURE FETCHER (no selector wiring here) ---
    def fetch_branches():
        ident = _parse_repo_identifier(State.repo_url)
        if not ident:
            ui.notify('Invalid repo. Use owner/repo or a GitHub URL', color='negative')
            return
        try:
            g = Github()  # public repos: no token required
            repo = g.get_repo(ident)
            branches = [b.name for b in repo.get_branches()]
            State.repo_branches = branches
            ui.notify('Repo ok ✓' if branches else 'No branches found', color='positive' if branches else 'warning')
            branch_selector.refresh()  # tell selector to re-render itself
        except Exception as e:
            State.repo_branches = []
            ui.notify(f'Error reading branches: {e}', color='negative')
            branch_selector.refresh()

    @ui.refreshable
    def branch_selector():
        """View-only selector; reads from State, does not fetch."""
        ui.select(options=State.repo_branches, with_input=False ).props('dense outlined').classes('w-full').bind_value(State, 'active_branch')

    @ui.refreshable
    def render():
        with ui.card().classes('w-full mx-auto p-4'):
            with ui.column().classes('w-full gap-3'):

                # App Directory (readonly) — bound to State
                ui.input('App Directory').props('dense outlined readonly').classes('w-full').bind_value(State, 'app_path')

                ui.separator()
                repo_input = ui.input('Github Repo') .props('dense outlined').classes('w-full').bind_value(State, 'repo_url')
                with repo_input.add_slot('append'):
                    ui.button(icon='search', on_click=fetch_branches).props('dense flat round').classes('q-ml-xs')
                with ui.row():
                    branch_selector()
                    ui.button('Clone')

    render()
    return render
