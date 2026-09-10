from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
@pytest.fixture 
def base_url():
    path = ROOT /"config"/"env.yaml"
    cfg = yaml.safe_load(path.read_text(encoding="utf-8"))
    return cfg["base_url"]

