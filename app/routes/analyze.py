from fastapi import APIRouter, Request,Depends

from app.middleware.jwt_auth import require_auth

router = APIRouter()

@router.get("/analyze/{sector}")
async def analyze_sector(sector: str, request: Request,user=Depends(require_auth)):
    return {"message": f"Analyzing sector: {sector}"}
