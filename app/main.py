#
from fastapi import FastAPI, HTTPException,Header
from pydantic import BaseModel
from common.db import query, execute

app = FastAPI()
users = {}
class RegisterIn(BaseModel):
    username:str
    password:str

class OrderIn(BaseModel):
    item: str
    qty: int

def _ensure_orders_table():
    execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT PRIMARY KEY AUTO_INCREMENT,
            item VARCHAR(64) NOT NULL,
            qty INT NOT NULL,
            owner VARCHAR(64) NOT NULL
        )
        """
    )
    try:
        execute(
            "ALTER TABLE orders ADD COLUMN owner VARCHAR(64) NOT NULL DEFAULT ''"
        )
    except Exception:
        pass

def _user_from_header(authorization: str | None):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing token")
    token = authorization.removeprefix("Bearer ")
    username = token.removeprefix("token-")
    if username not in users:
        raise HTTPException(status_code=401, detail="bad token")
    return username

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-ping")
def db_ping():
    rows = query("SELECT 1 AS ok")
    return rows[0]

@app.post("/orders")
def create_order(body: OrderIn, authorization: str | None = Header(default=None)):
    username = _user_from_header(authorization)
    if body.qty < 1:
        raise HTTPException(status_code=400, detail="qty must be >= 1")
    _ensure_orders_table()
    order_id = execute(
        "INSERT INTO orders (item, qty, owner) VALUES (%s, %s, %s)",
        (body.item, body.qty, username),
    )
    return {"id": order_id, "item": body.item, "qty": body.qty}

@app.get("/orders/{order_id}")
def get_order(order_id: int, authorization: str | None = Header(default=None)):
    username = _user_from_header(authorization)
    _ensure_orders_table()
    rows = query("SELECT id, item, qty, owner FROM orders WHERE id = %s", (order_id,))
    if not rows:
        raise HTTPException(status_code=404, detail="order not found")
    if rows[0]["owner"] != username:
        raise HTTPException(status_code=403, detail="forbidden")
    return {"id": rows[0]["id"], "item": rows[0]["item"], "qty": rows[0]["qty"]}

@app.post("/register")
def register(body: RegisterIn):
    if body.username in users:
        raise HTTPException(status_code=400, detail="username exists")
    users[body.username] = body.password
    return {"username": body.username}

@app.post("/login")
def login(body: RegisterIn):
    if users.get(body.username) != body.password:
        raise HTTPException(status_code=401, detail="bad credentials")
    return {"token": f"token-{body.username}"}

@app.get("/me")
def me(authorization: str | None = Header(default=None)):
    username = _user_from_header(authorization)
    return {"username": username}
