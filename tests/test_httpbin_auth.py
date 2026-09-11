from common.http_client import get

def test_httpbin_get_carries_bearer(base_url, auth_token):
    url = f"{base_url}/get"
    response = get(url)
    assert response.status_code == 200
    body = response.json()
    assert body["headers"]["Authorization"] == f"Bearer {auth_token}"