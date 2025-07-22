
import os
import jwt
from passlib.hash import bcrypt
from datetime import datetime, timedelta
from app.models.user_store import users

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_EXPIRY = timedelta(days=2)

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
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + JWT_EXPIRY
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def decode_jwt(token: str) -> str:
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
