[![Python application](https://github.com/zimzf23/App-Deployer/actions/workflows/python-app.yml/badge.svg)](https://github.com/zimzf23/App-Deployer/actions/workflows/python-app.yml)
# App Deployer

A lightweight developer tool built with [NiceGUI](https://nicegui.io/) to simplify **server-side app deployment workflows**.  

App Deployer provides:
- A **filesystem picker** with neon-dark UI for selecting root, app, code, backup, and archive folders.
- A **nuclear wipe** function to safely and instantly clear selected directories before redeploy (avoids leftover contamination).
- **GitHub integration**: fetch branches from a repo, pick one, and clone it directly into your selected target directory.
- A unified **dark dashboard** with modular sections for Filesystem, Source Control, Services, and IIS.

---

## Features

### Filesystem Management
- Interactive folder pickers with dialogs (bound to global `State`).
- Root-aware browsing that ensures all other pickers open under the chosen root path.
- One-click wipe (`💣`) using PowerShell `Remove-Item -Recurse -Force`.
- Dedicated inputs for:
  - Root folder
  - App folder
  - Code folder
  - Backup folder
  - Archive folder

### Source Control
- Input any public GitHub repo (full URL or `owner/repo`).
- Fetch available branches via the GitHub API.
- Select and clone a branch into your target directory (`git clone` via subprocess).
- Integrated branch selector + “Clone” button.

### UI
- Built with [NiceGUI](https://nicegui.io/).
- Dark mode with neon green theme.
- Custom banners and section headers for a clean dashboard experience.

---

## Project Structure

```
.
├── Deployer_v1.py      # Main entry point, defines pages
├── dependencies.py     # Shared imports and asset setup
├── layouts.py          # Styles and headers
├── state.py            # Global State class (paths, repo info, etc.)
├── filesys.py          # Filesystem picker and wipe logic
├── source.py           # GitHub integration and branch selector
└── assets/             # Images, fonts, banner
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Git installed and available in PATH
- PowerShell (on Windows)

### Install dependencies
```bash
pip install nicegui PyGithub
```

### Run the app
```bash
python Deployer_v1.py
```

By default it starts at:
```
http://127.0.0.1:8000
```

---

## Usage

1. **Filesystem**  
   - Select a root folder  
   - Pick App / Code / Backup / Archive directories under that root  
   - Use **Wipe** to clear them before redeploying  

2. **Source Control**  
   - Enter a GitHub repo (`https://github.com/user/repo` or `user/repo`)  
   - Fetch available branches  
   - Select a branch and click **Clone** to deploy into your selected folder  

3. **Other Sections**  
   - Services and IIS pages are placeholders for expansion  

---

## Roadmap
- Add **confirmation dialog** for destructive wipes (optional safety).
- Add **auto redeploy pipeline**: Wipe → Clone → Run setup script.
- Add **service manager** for background tasks.

---

## License
TBD
