from fastapi import APIRouter, HTTPException, Request,Depends
from fastapi.responses import  PlainTextResponse

from app.middleware.jwt_auth import require_auth
from app.services.analyze_service import analyze_sector, validate_sector

router = APIRouter()

@router.get("/analyze/{sector}")
async def analyze(sector: str, request: Request,user=Depends(require_auth)):
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
