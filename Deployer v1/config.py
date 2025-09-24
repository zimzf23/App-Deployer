from dependencies import *
from state import State


CONFIG_FILENAME = 'Configuration.toml'

def _discover_fields() -> list[str]:
    """All non-private, non-callable attributes on State (class-level)."""
    return [k for k, v in vars(State).items() if not k.startswith('_') and not callable(v)]

def _to_dict() -> dict:
    """Serialize State -> plain dict."""
    data = {}
    for k in _discover_fields():
        v = getattr(State, k)
        if isinstance(v, Path):
            v = str(v)
        data[k] = v
    return data

def _apply_dict(d: dict) -> None:
    """Apply dict -> State."""
    for k in _discover_fields():
        if k in d:
            setattr(State, k, d[k])

def _config_path() -> Path:
    """<root_path>/Configuration.toml (requires State.root_path)."""
    root = getattr(State, 'root_path', '') or ''
    if not root:
        raise ValueError('State.root_path is not set')
    return Path(root).resolve() / CONFIG_FILENAME

def check_configuration_exists() -> bool:
    """
    Check if <root>/Configuration.toml exists.
    If missing, just notify (as requested). Returns True/False.
    """
    try:
        cfg = _config_path()
    except ValueError:
        ui.notify('Set a Root path first', color='warning')
        return False

    if not cfg.exists():
        ui.notify(f'Missing {CONFIG_FILENAME} in {cfg.parent}', color='warning')
        return False
    return True

def save_configuration(overwrite: bool = True) -> bool:
    """
    Create/overwrite <root>/Configuration.toml with current State values.
    Returns True on success.
    """
    try:
        cfg = _config_path()
    except ValueError:
        ui.notify('Set a Root path first', color='warning')
        return False

    cfg.parent.mkdir(parents=True, exist_ok=True)
    if cfg.exists() and not overwrite:
        ui.notify(f'{CONFIG_FILENAME} already exists (not overwritten)', color='warning')
        return False

    try:
        with open(cfg, 'w', encoding='utf-8') as f:
            toml.dump(_to_dict(), f)
        ui.notify(f'Saved {CONFIG_FILENAME}', color='positive')
        return True
    except Exception as e:
        ui.notify(f'Failed to save config: {e}', color='negative')
        return False

def load_configuration() -> bool:
    """
    If <root>/Configuration.toml exists, read it and apply into State.
    If not found, only notify. Returns True if loaded, False otherwise.
    """
    try:
        cfg = _config_path()
    except ValueError:
        ui.notify('Set a Root path first', color='warning')
        return False

    if not cfg.exists():
        ui.notify(f'{CONFIG_FILENAME} not found in {cfg.parent}', color='warning')
        return False

    try:
        data = toml.load(cfg)
        if isinstance(data, dict):
            _apply_dict(data)
            ui.notify(f'Loaded {CONFIG_FILENAME}', color='positive')
            return True
        else:
            ui.notify('Invalid configuration format', color='negative')
            return False
    except Exception as e:
        ui.notify(f'Failed to load config: {e}', color='negative')
        return False