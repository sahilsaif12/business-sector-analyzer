from fastapi import APIRouter, HTTPException, Request,Depends

from app.lib.gemini import askAi
from app.lib.prompts import sector_validation_prompt
from app.middleware.jwt_auth import require_auth

router = APIRouter()

@router.get("/analyze/{sector}")
async def analyze_sector(sector: str, request: Request,user=Depends(require_auth)):
    if not sector:
        raise HTTPException(status_code=400, detail="Sector is required")
    sectorValidationPrompt = sector_validation_prompt(sector)
    sectorValidationResponse = askAi(sectorValidationPrompt)

    if not sectorValidationResponse:
        raise HTTPException(status_code=500, detail="There is some issue with the AI service. Please try again after some time.")
    
    if sectorValidationResponse.startswith("valid"):
        return {"message": f" {sector} is a valid sector and can be analyzed."}
    else:
        raise HTTPException(status_code=400, detail=f"{sector} is a invalid sector:. Please provide a valid sector for analysis.")
   
    return {"message": f"Analyzing sector: {sector}"}
