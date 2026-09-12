from common.db import query,execute
import pytest

def test_devices_count():
    rows = query("SELECT COUNT(*) AS n FROM devices")
    assert rows[0]["n"] == 3

@pytest.fixture
def tmp_device():
    execute(
        "INSERT INTO devices (name, status) VALUES (%s, %s)",
        ("qa-tmp-01", "online"),
    )
    yield "qa-tmp-01"
    execute("DELETE FROM devices WHERE name = %s", ("qa-tmp-01",))

def test_tmp_device_exists(tmp_device):
    rows = query("SELECT * FROM devices WHERE name = %s", (tmp_device,))
    assert rows[0]["status"] == "online"

@pytest.fixture
def tmp_order():
    order_id = execute(
        "INSERT INTO orders (device_id, amount) VALUES (%s, %s)",
        (2,99),
    )
    yield {"id": order_id, "device_id": 2, "amount": 99}
    execute("DELETE FROM orders WHERE id = %s", (order_id,))

def test_create_order_matched(tmp_order):
    rows = query("SELECT device_id,amount FROM orders WHERE id = %s", (tmp_order["id"],))
    assert rows[0]["device_id"] == tmp_order["device_id"]
    assert rows[0]["amount"] == tmp_order["amount"]