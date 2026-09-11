import time
from pathlib import Path

import requests
import yaml
from requests.exceptions import RequestException

ROOT = Path(__file__).resolve().parents[1]
_cfg = yaml.safe_load(
    (ROOT / "config" / "env.yaml").read_text(encoding="utf-8")
)
TIMEOUT = _cfg["timeout"]
DEFAULT_HEADERS = {"Accept": "application/json"}
_token = None

def set_token(token):
    global _token
    _token = token


def _send(method, url, timeout=None, **kwargs):
    if timeout is None:
        timeout = TIMEOUT
    headers = dict(DEFAULT_HEADERS)
    extra = kwargs.pop("headers", None)
    if extra:
        headers.update(extra)
    kwargs["headers"] = headers
    if _token:
        headers.setdefault("Authorization", f"Bearer {_token}")

    start = time.perf_counter()
    try:
        response = requests.request(method, url, timeout=timeout, **kwargs)
    except RequestException as e:
        raise RuntimeError(f"{method} {url} failed: {e}") from e
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"{method} {url} -> {response.status_code} ({elapsed_ms:.0f}ms)")
    return response


def get(url, timeout=None, **kwargs):
    return _send("GET", url, timeout, **kwargs)

def post_json(url, json, timeout=None, **kwargs):
    return _send("POST", url, timeout, json=json, **kwargs)