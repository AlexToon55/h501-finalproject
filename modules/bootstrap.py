""" Module to set up the project environment."""
from pathlib import Path
import sys

def add_project_root():
    root = Path(__file__).resolve().parents[1]
    if str(root) not in sys.path:
        sys.path.append(str(root))
add_project_root()