# report/utils.py
from __future__ import annotations
from pathlib import Path
import pickle
from typing import Any

# Path vars required by the project rubric
PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "assets" / "model.pkl"

def load_model() -> Any:
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


#from pathlib import Path

#project_root = Path(__file__).resolve().parent.parent
#package_path = project_root / 'python-package' / 'employee_events'

#event_color = '\033[96m'
#complete_color = '\033[92m'
#color_end = '\033[0m'
