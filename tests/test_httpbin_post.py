import pytest
import yaml
from pathlib import Path
from common.http_client import post_json

def test_httpbin_post_json(base_url):
    url = f"{base_url}/post"
    headers = {"Content-Type": "application/json"}
    json = {"username": "admin", "password": "123456"}
    response = post_json(url, json, headers=headers)

    assert response.status_code == 200
    body = response.json()
    assert body["json"]["username"] == "admin"
    assert body["json"]["password"] == "123456"

def _username_cases():
    path = Path(__file__).resolve().parents[1] / "data" / "post_username_cases.yaml"
    rows = yaml.safe_load(path.read_text(encoding="utf-8"))
    return[(row["payload"], row["expected_username"]) for row in rows]

@pytest.mark.parametrize("payload,expected_username",_username_cases())

def test_httpbin_post_username_case(base_url, payload, expected_username):
    url = f"{base_url}/post"
    response = post_json(url, payload)
    assert response.status_code == 200
    body = response.json()
    assert body["json"].get("username") == expected_username    