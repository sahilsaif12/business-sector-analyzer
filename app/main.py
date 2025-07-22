
from fastapi import FastAPI
from app.routes import analyze, auth

app = FastAPI(title="Market Data Analyze API")

app.include_router(auth.router)
app.include_router(analyze.router)

@app.get("/")
def root():
    return {"message": "Market Insights API is running"}
