from common.assertions import assert_json, assert_status
from common.db import query
from common.http_client import get, post_json

APP = "http://127.0.0.1:8000"

def test_create_and_get_order():
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

def test_get_order_missing():
    response = get(f"{APP}/orders/999999")
    assert_status(response, 404)

def test_create_order_qty_invalid():
    response = post_json(f"{APP}/orders", {"item": "book", "qty": 0})
    assert_status(response, 400)

def test_create_order_matches_db(monkeypatch):
    monkeypatch.setenv("MYSQL_HOST", "127.0.0.1")
    monkeypatch.setenv("MYSQL_PORT", "3307")
    created = post_json(f"{APP}/orders", {"item": "pen", "qty": 3})
    assert_status(created)
    order_id = created.json()["id"]
    rows = query("SELECT id, item, qty FROM orders WHERE id = %s", (order_id,))
    assert len(rows) == 1
    assert rows[0]["id"] == order_id
    assert rows[0]["item"] == "pen"
    assert rows[0]["qty"] == 3
