import requests
import pytest

@pytest.mark.smoke
def test_httpbin_get_foo(base_url):
    url = f"{base_url}/get?foo=1"
    response = requests.get(url, timeout=10)

    assert response.status_code == 200,(
        f"url={url}, status={response.status_code} body={response.text}")
    body = response.json()
    assert body["args"]["foo"] == "1"
