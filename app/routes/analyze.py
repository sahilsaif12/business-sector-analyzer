from datetime import datetime
from fastapi import APIRouter, HTTPException, Request,Depends
from fastapi.responses import  PlainTextResponse

from app.middleware.jwt_auth import require_auth
from app.middleware.rate_limiter import rate_limiter
from app.models.user_store import users
from app.services.analyze_service import analyze_sector, validate_sector

router = APIRouter()
MAX_API_CALLS_PER_SESSION=10

@router.get("/analyze/{sector}")
async def analyze(sector: str, request: Request,user_email=Depends(require_auth),_=Depends(rate_limiter)):
    # session usage tracking
    session = users.get(user_email, {}).get("session")
    if session:
        
        if "usage" not in session:
            session["usage"] = {
                "analyze_calls": 0,
                "last_call_at": None
            }

        if session["usage"]["analyze_calls"] >= MAX_API_CALLS_PER_SESSION:
            raise HTTPException(
                status_code=429,
                detail=f"Session usage limit exceeded for analyzing sector."
            )

        session["usage"]["analyze_calls"] += 1
        session["usage"]["last_call_at"] = datetime.utcnow().isoformat()

    if not sector:
        raise HTTPException(status_code=400, detail="Sector is required")
    isSectorValid=validate_sector(sector)
    # If the AI service fails to respond, we return None
    if isSectorValid is None:
        raise HTTPException(status_code=500, detail="There is some issue with the AI service. Please try again after some time.")
    # AI said the sector is not a vaild sector to analyze
    if not isSectorValid:
        raise HTTPException(status_code=400, detail=f"{sector} is a invalid sector:. Please provide a valid sector for analysis.")
       
    markdown_report = analyze_sector(sector)

    if markdown_report:
        return PlainTextResponse(content=markdown_report)
    else:
        return {"message": f"could not analyze for {sector} sector due to AI models unavailability . Please try again after some time."}
