import pytest
from common.http_client import get
from common.assertions import assert_status, assert_json

@pytest.mark.smoke
def test_httpbin_get_foo(base_url):
    url = f"{base_url}/get?foo=1"
    response = get(url)
    assert_status(response)
    body = response.json()
    assert_json(body, "headers.Accept", "application/json")
    assert_json(body, "args.foo", "1")