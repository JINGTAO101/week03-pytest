from common.http_client import get
from common.assertions import assert_status

def test_httpbin_get_carries_bearer(base_url, auth_token):
    url = f"{base_url}/get"
    response = get(url)
    assert_status(response)
    body = response.json()
    assert body["headers"]["Authorization"] == f"Bearer {auth_token}"