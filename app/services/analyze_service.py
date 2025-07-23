


from app.lib.gemini import askAi
from app.lib.prompts import sector_validation_prompt
from app.lib.webSearch import getRecentNews
import json
import os


def validate_sector(sector: str) -> bool:
    prompt = sector_validation_prompt(sector)
    response = askAi(prompt)

    if not response:
        return None  # indicates Ai failure
    return response.lower().startswith("valid")

def analyze_sector(sector: str) -> str:
    # Step 1: Try web search
    articles = getRecentNews(sector)
    root_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = os.path.abspath(os.path.join(root_dir, "../../articles.json"))

    with open(root_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    return True