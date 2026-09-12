#
import uuid
from common.assertions import assert_json,assert_status
from common.http_client import get,post_json,set_token

APP = "http://127.0.0.1:8000"

def test_health():
    response = get(f"{APP}/health")
    assert_status(response)
    assert_json(response.json(),"status","ok")

def test_register_login_me():
    name = f"qa-{uuid.uuid4().hex[:8]}"
    response = post_json(f"{APP}/register",{"username":name,"password":"123456"})
    assert_status(response)
    assert_json(response.json(),"username",name)

    response = post_json(f"{APP}/login",{"username":name,"password":"123456"})
    assert_status(response)
    token = response.json()["token"]

    set_token(token)
    try:
        response = get(f"{APP}/me")
        assert_status(response)
        assert_json(response.json(),"username",name)
    finally:
        set_token(None)

def test_me_missing_token():
    set_token(None)
    response = get(f"{APP}/me")
    assert_status(response,401)