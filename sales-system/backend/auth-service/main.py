from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta

# ======================
# CONFIG
# ======================
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="Auth Service")

# ======================
# MODELS
# ======================
class LoginRequest(BaseModel):
    username: str
    password: str

# ======================
# ROOT (test endpoint)
# ======================
@app.get("/")
def root():
    return {"status": "auth-service running"}

# ======================
# LOGIN
# ======================
@app.post("/login")
def login(data: LoginRequest):
    # DEMO user (mjafton për projekt)
    if data.username != "admin" or data.password != "admin":
        raise HTTPException(status_code=401, detail="Invalid credentials")

    payload = {
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }
