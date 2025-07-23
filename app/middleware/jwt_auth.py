
from datetime import datetime
from fastapi import Request, HTTPException
from jwt import ExpiredSignatureError
from app.models.user_store import users
from app.services.auth_service import decode_jwt

def require_auth(request: Request):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated to access this , please login with correct credentials")

    try:
        payload = decode_jwt(token)
        email = payload["sub"]

        # do user exists?
        if email not in users:
            raise HTTPException(status_code=401, detail="User not found, create one")

        session = users[email].get("session")

        # Check session exists
        if not session:
            raise HTTPException(status_code=401, detail="No active session found , please login again")

        # Check token match
        if session.get("token") != token:
            raise HTTPException(status_code=401, detail="Token got tempered, please login again")

        # Checking is token expired?
        expires_at = datetime.fromisoformat(session["expires_at"])
        if datetime.utcnow() > expires_at:
            raise HTTPException(status_code=401, detail="Session has expired, please login again")

        return email  

    except ExpiredSignatureError:
        raise HTTPException(status_code=400, detail="Session has expired, please login again")
    except Exception as e :
        print("error",e)
        raise HTTPException(status_code=401, detail="Invalid or expired token, please login again")
