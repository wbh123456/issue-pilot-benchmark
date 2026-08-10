"""Pytest bootstrap: make the repository root importable so tests can do
``from app.main import app`` regardless of the caller's cwd."""

import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
