
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel,EmailStr
from app.middleware.jwt_auth import require_auth
from app.services.auth_service import *

router = APIRouter(prefix="/auth", tags=["auth"])

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
def login(auth: AuthRequest):
    if not auth.email or not auth.password:
        raise HTTPException(status_code=400, detail="Email and password are required")
    user = get_user(auth.email)

    if user:
        if not verify_password(auth.password, user["password"]):
            raise HTTPException(status_code=401, detail="Wrong password")
    else:
        create_user(auth.email, auth.password)

    token = create_jwt(auth.email)
    response = JSONResponse({"message": "you are logged in"})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=True,  
        samesite="Strict"
    )
    return response



@router.post("/logout")
def logout(request: Request, response: Response, user_email=Depends(require_auth)):
    clearSession(user_email)
    response.delete_cookie("access_token")
    return {"message": "you are Logged out successfully"}