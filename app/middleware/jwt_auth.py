
from fastapi import Request, HTTPException
from app.services.auth_service import decode_jwt

def require_auth(request: Request):
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated to access this , please login with correct credentials")

    try:
        payload = decode_jwt(token)
        return payload["sub"]  # user email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
