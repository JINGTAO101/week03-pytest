import uuid

from common.assertions import assert_json, assert_status
from common.db import query
from common.http_client import get, post_json, set_token

APP = "http://127.0.0.1:8000"


def _login():
    name = f"qa-{uuid.uuid4().hex[:8]}"
    registered = post_json(f"{APP}/register", {"username": name, "password": "123456"})
    assert_status(registered)
    logged_in = post_json(f"{APP}/login", {"username": name, "password": "123456"})
    assert_status(logged_in)
    set_token(logged_in.json()["token"])
    return name


def test_create_order_unauthorized():
    set_token(None)
    response = post_json(f"{APP}/orders", {"item": "book", "qty": 2})
    assert_status(response, 401)


def test_create_and_get_order():
    _login()
    try:
        created = post_json(f"{APP}/orders", {"item": "book", "qty": 2})
        assert_status(created)
        body = created.json()
        assert_json(body, "item", "book")
        assert_json(body, "qty", 2)
        order_id = body["id"]

        fetched = get(f"{APP}/orders/{order_id}")
        assert_status(fetched)
        assert_json(fetched.json(), "id", order_id)
        assert_json(fetched.json(), "item", "book")
        assert_json(fetched.json(), "qty", 2)
    finally:
        set_token(None)


def test_get_order_missing():
    _login()
    try:
        response = get(f"{APP}/orders/999999")
        assert_status(response, 404)
    finally:
        set_token(None)


def test_get_order_forbidden():
    _login()
    try:
        created = post_json(f"{APP}/orders", {"item": "book", "qty": 2})
        assert_status(created)
        order_id = created.json()["id"]
    finally:
        set_token(None)

    _login()
    try:
        response = get(f"{APP}/orders/{order_id}")
        assert_status(response, 403)
    finally:
        set_token(None)


def test_create_order_qty_invalid():
    _login()
    try:
        response = post_json(f"{APP}/orders", {"item": "book", "qty": 0})
        assert_status(response, 400)
    finally:
        set_token(None)


def test_create_order_matches_db(monkeypatch):
    monkeypatch.setenv("MYSQL_HOST", "127.0.0.1")
    monkeypatch.setenv("MYSQL_PORT", "3307")
    _login()
    try:
        created = post_json(f"{APP}/orders", {"item": "pen", "qty": 3})
        assert_status(created)
        order_id = created.json()["id"]
        rows = query("SELECT id, item, qty FROM orders WHERE id = %s", (order_id,))
        assert len(rows) == 1
        assert rows[0]["id"] == order_id
        assert rows[0]["item"] == "pen"
        assert rows[0]["qty"] == 3
    finally:
        set_token(None)
