import pytest
import yaml
from pathlib import Path
from common.http_client import post_json
from common.assertions import assert_status,assert_json

def test_httpbin_post_json(base_url):
    url = f"{base_url}/post"
    headers = {"Content-Type": "application/json"}
    json = {"username": "admin", "password": "123456"}
    response = post_json(url, json, headers=headers)
    assert_status(response)
    body = response.json()
    assert_json(body, "json.username", "admin")
    assert_json(body, "json.password", "123456")

def _username_cases():
    path = Path(__file__).resolve().parents[1] / "data" / "post_username_cases.yaml"
    rows = yaml.safe_load(path.read_text(encoding="utf-8"))
    return[(row["payload"], row["expected_username"]) for row in rows]

@pytest.mark.parametrize("payload,expected_username",_username_cases())

def test_httpbin_post_username_case(base_url, payload, expected_username):
    url = f"{base_url}/post"
    response = post_json(url, payload)
    assert_status(response)
    body = response.json()
    assert_json(body, "json.username", expected_username)    