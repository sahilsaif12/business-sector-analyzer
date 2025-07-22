from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/analyze/{sector}")
async def analyze_sector(sector: str, request: Request):
    return {"message": f"Analyzing sector: {sector}"}
