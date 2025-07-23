from serpapi import GoogleSearch
import os

params = {
  "api_key": os.getenv("SERPAPI_API_KEY"),
  "engine": "google_news",
  "hl": "en",
  "gl": "in",
}

def getRecentNews(sector:str,num_results: int = 20):
    if not sector:
        return None
    params["q"] = f"recent news on {sector} sector"

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        print("results",results)

        # Extract structured recent news data for feeding to Gemini for better analysis
        articles = results.get("news_results", [])[:num_results]
        cleaned_articles = []

        for article in articles:
            cleaned = {
                "title": article.get("title"),
                "source": article.get("source", {}).get("name"),
                "date": article.get("date"),
                "link": article.get("link")
            }
            if cleaned["title"]:  # Only include if there's a title
                cleaned_articles.append(cleaned)

        if not cleaned_articles:
            print("No valid recent news articles found regarding that sector via web search .")
        print("cleaned_articles",cleaned_articles)
        return cleaned_articles

    except Exception as e:
        print(f"[SerpAPI Exception] Failed to fetch news: {e}")
        return []
