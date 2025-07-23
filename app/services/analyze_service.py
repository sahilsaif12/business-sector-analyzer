


from app.lib.gemini import askAi
from app.lib.prompts import full_sector_analysis_prompt, sector_validation_prompt
from app.lib.webSearch import getRecentNews


def validate_sector(sector: str) -> bool:
    prompt = sector_validation_prompt(sector)
    response = askAi(prompt)

    if not response:
        return None  # indicates Ai failure
    return response.lower().startswith("valid")

def analyze_sector(sector: str) -> str:
    # Step 1: Try web search
    articles = getRecentNews(sector)

  # Step 2: Create prompt for Gemini
    prompt = full_sector_analysis_prompt(sector, articles)

    # Step 3: Ask Ai
    markdown = askAi(prompt)
    return markdown
    

