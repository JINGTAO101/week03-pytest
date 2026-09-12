from pathlib import Path

import pytest
import yaml

from common.assertions import assert_json,assert_status,assert_len
from common.http_client import get

def _query_case():
    path = Path(__file__).resolve().parents[1]/"data"/"get_query_cases.yaml"
    rows = yaml.safe_load(path.read_text(encoding="utf-8"))
    return[(row["params"],row["path"],row["expected"]) for row in rows]

@pytest.mark.parametrize("params,path,expected",_query_case())
def test_httpbin_get_query_case(base_url,params,path,expected):
    url = f"{base_url}/get"
    response = get(url,params=params)
    assert_status(response)
    body = response.json()
    assert_json(body,path,expected)

def test_httpbin_get_args_count(base_url):
    url = f"{base_url}/get"
    response = get(url,params = {"foo":"1","bar":"2"})
    assert_status(response)
    body = response.json()
    assert_len(body,"args",2)