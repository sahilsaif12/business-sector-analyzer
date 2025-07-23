
def sector_validation_prompt(sector: str) -> str:
    return (
        f'You are a business analyst. Is "{sector}" a valid business or industrial sector in India or in the world?\n'
        f'Reply strictly with "valid" or "invalid".'
    )

def full_sector_analysis_prompt(sector: str, articles: list[dict]) -> str:
    base = f"""
You are a senior business research analyst specializing in Indian industry sectors.

Your task is to produce a detailed, structured, and up-to-date **markdown-formatted** report on the **{sector}** sector in India.

---

###  Guidelines:

- Use **only markdown syntax**.
- Explore and reference **article titles** and **linked URLs** provided below.
- Include **quantitative insights** like market size, revenue growth, export/import trends, YoY growth, CAGR if available.
- Provide strategic observations based on recent news and industry momentum.
- Make the tone business-grade, suitable for investors or market analysts.

---

###  Report Structure:

#### # Market Overview
- What is the current size and scope of the sector in India?
- Recent historical data or performance indicators

#### ## Recent Developments
- Bullet points of major announcements, policy changes, tech shifts, and innovations
- Use recent news (titles and links) to support claims

#### ## Key Players
- Top companies operating in this sector
- Their role, market share, and recent moves

#### ## Investment & Trade Opportunities
- Where investors or exporters/importers can find growth
- Regulatory changes aiding this

#### ## Emerging Trends
- Technology, startups, demand-side changes, global influences

#### ## Challenges & Risks
- Policy bottlenecks, resource shortages, geopolitical risks

#### ## Strategic Insights
- Analyst-style commentary with 2–3 key takeaways

#### ## Source Summary
- Cite the news article titles and link (use markdown `[]()` syntax)
"""

    if articles:
        base += "\n\n---\n\n###  Articles for Context (go through the resources and explored them deeply, your reports should back by datas and sources):\n"
        for article in articles:
            base += f'- [{article["title"]}]({article["link"]}) — {article["source"]} ({article["date"]})\n'

    else:
        base += "\n\n---\n\nNo news articles were found for this sector. You may proceed with historical + market-based insights instead.\n"

    return base.strip()
