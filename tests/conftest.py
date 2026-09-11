from pathlib import Path

import pytest
import yaml
from common.settings import load_cfg
from common.http_client import set_token


@pytest.fixture
def base_url():
    return load_cfg()["base_url"]

@pytest.fixture
def auth_token():
    token = "demo-token"
    set_token(token)
    yield token
    set_token(None)

