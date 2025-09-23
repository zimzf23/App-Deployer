from __future__ import annotations
from nicegui import ui, app, events

import os
import sys

from pathlib import Path
import time

# Determine where the bundled assets actually live:
if getattr(sys, "_MEIPASS", None):
    # Running as a bundled exe
    assets_path = os.path.join(sys._MEIPASS, "assets")
else:
    # Running from source
    assets_path = os.path.join(os.path.dirname(__file__), "assets")

# Serve everything under that folder at /assets
app.add_static_files("/assets", assets_path)