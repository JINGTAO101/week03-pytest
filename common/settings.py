import os
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

def load_cfg():
    name = os.environ.get("TEST_ENV", "test")
    path = ROOT / "config" / f"{name}.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))