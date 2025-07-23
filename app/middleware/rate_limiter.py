
from fastapi import Request, HTTPException
from typing import Dict, List
import time

# Track API usage in-memory 
rate_limit_store: Dict[str, List[float]] = {}

# Configurable rate limits for per 
RATE_LIMIT = 3  # Max requests
RATE_WINDOW = 60  # In seconds

def rate_limiter(request: Request):
    # Key:  user's email 
    key = request.state.user_email 

    now = time.time()
    window_start = now - RATE_WINDOW

    if key not in rate_limit_store:
        rate_limit_store[key] = []

    # Remove outdated requests
    recent_requests = [t for t in rate_limit_store[key] if t > window_start]
    rate_limit_store[key] = recent_requests

    if len(recent_requests) >= RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again after a minute."
        )

    rate_limit_store[key].append(now)
