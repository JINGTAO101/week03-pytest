#
from fastapi import FastAPI, HTTPException,Header
from pydantic import BaseModel

app = FastAPI()
users = {}
class RegisterIn(BaseModel):
    username:str
    password:str

@app.get("/health")
def health():
    return {"status": "ok"}

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
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="missing token")
    token = authorization.removeprefix("Bearer ")
    username = token.removeprefix("token-")
    if username not in users:
        raise HTTPException(status_code=401, detail="bad token")
    return {"username": username}
