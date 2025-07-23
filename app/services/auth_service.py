
import os
import jwt
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from app.models.user_store import users

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRY = timedelta(minutes=int(os.getenv("JWT_EXPIRY",20)) ) # Default to 20 minutes if not set
def get_user(email: str):
    return users.get(email)

def create_user(email: str, password: str):
    users[email] = {
        "password": bcrypt.hash(password),
        "session": {}
    }

def verify_password(raw_password: str, hashed_password: str) -> bool:
    return bcrypt.verify(raw_password, hashed_password)

def create_jwt(email: str) -> str:
    expires_at= datetime.utcnow() + JWT_EXPIRY
    payload = {
        "sub": email,
        "exp":expires_at
    }

    token=jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    users[email]["session"] = {
        "token": token,
        "issued_at": datetime.utcnow().isoformat(),
        "expires_at": expires_at.isoformat()
    }
    return token

def decode_jwt(token: str) -> str:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

def clearSession(email:str):
    users[email]["session"] = {}