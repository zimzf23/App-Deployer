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

    def run_cmd(*args):
        r = subprocess.run(args, text=True, capture_output=True)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip() or f'Command failed: {" ".join(args)}')
        return r.stdout.strip()

    def clone_repo():
        if not State.repo_url:
            ui.notify('No repo URL', color='negative'); return
        if not State.active_branch:
            ui.notify('No branch selected', color='negative'); return
        if not State.root_path:
            ui.notify('No target directory', color='negative'); return

        target = Path(State.root_path)
        if target.exists() and any(target.iterdir()):
            ui.notify('Target folder not empty', color='warning')
            return

        try:
            ui.notify(f'Cloning {State.repo_url}@{State.active_branch} …', color='primary')
            run_cmd('git', 'clone', '--branch', State.active_branch, State.repo_url, str(target))
            ui.notify(f'Cloned to {target}', color='positive')
        except Exception as e:
            ui.notify(f'Clone failed: {e}', color='negative')

    @ui.refreshable
    def branch_selector():
        """View-only selector; reads from State, does not fetch."""
        ui.select(options=State.repo_branches, with_input=False ).props('dense outlined').bind_value(State, 'active_branch').classes('flex-1')

    @ui.refreshable
    def render():
        with ui.card().classes('w-full mx-auto p-4'):
            with ui.column().classes('w-full gap-3'):

                # App Directory (readonly) — bound to State
                ui.input('App Directory').props('dense outlined readonly').classes('w-full').bind_value(State, 'root_path')

                ui.separator()
                repo_input = ui.input('Github Repo') .props('dense outlined').classes('w-full').bind_value(State, 'repo_url')
                with repo_input.add_slot('append'):
                    ui.button(icon='search', on_click=fetch_branches).props('dense flat round').classes('q-ml-xs')
                with ui.row().classes('gap-10 flex-nowrap w-full'):
                    branch_selector()
                    ui.button('Clone', on_click=clone_repo)

    render()
    return render
