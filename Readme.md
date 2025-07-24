#  Business Sector Analyzer 

An intelligent API system that leverages **Google Gemini** and **SerpAPI** to validate user-defined sectors, fetch relevant recent news on that sector, and generate in-depth, markdown-formatted analytical reports. Built with **FastAPI**,  includes secure **JWT-based authentication**, **session tracking**, and **rate limiting**.

---

### see sample output results
[check here](https://github.com/sahilsaif12/business-sector-analyzer/tree/main/sampleOutputs)


---
### Live deployed link

(service deployed to render, so sometime its basically take 50-60 sec downtime because of inactivity, so requesting you wait 50-60 secs for spin up the service if its goes down due to inactivity)
[live here](https://business-sector-analyzer.onrender.com/)

[for swagger testing check this](https://business-sector-analyzer.onrender.com/docs)

---
### see the demo video
[watch the loom](https://www.loom.com/share/92aa6de6a07d44d6a4fc7df774330f06?sid=8b2b52cf-642f-42d7-84f9-3bfc5c82b378)




---
https://business-sector-analyzer.onrender.com/
##  Key Achieved parts

- ✅ **Single endpoint login/registration with JWT**
- ✅ **Protected routes using session cookies**
- ✅ **Sector validation using Google Gemini (LLM)**
- ✅ **Web search using SerpAPI (Google News)**
- ✅ **Dynamic, markdown-formatted sector analysis reports as response**
- ✅ **Session-based usage tracking**
- ✅ **Rate limiting per user to prevent abuse** (3 req/min) [as the analysis itself will take time so a number like 5 or 10 in 60sec will be unrealistic]
- ✅ **Full error handling, retry mechanisms, and fallbacks**
- ✅ **Clean Modular Structure**


---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sahilsaif12/business-sector-analyzer

```

### 2. Create Python Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate #(on windows)
```

### 3. Install Requirements
```bash
pip install -r requirements.txt

```

### 4. Create `.env` File and copy the keys from `.env.sample`
```env
GEMINI_API_KEY=gemini_api_key
SERPAPI_API_KEY=serpapi_api_key
JWT_SECRET=secret-key
JWT_EXPIRY=number-of-minutes
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload
```

### Now the app should be live
Visit: [http://localhost:8000](http://localhost:8000)

for docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🚀 Tech Stack

| Layer             | Tool/Library                   |
|------------------|-------------------------------|
| Framework        | FastAPI                        |
| AI/LLM           | Google Gemini via `google-genai` |
| Web Search       | SerpAPI (Google News Engine)   |
| Auth             | JWT with HttpOnly Cookies      |
| Rate Limiting    | In-memory |
| Dependency Mgmt  | `requirements.txt`             |

---

## 🗂 Folder Structure

```
app/
├── main.py                  # App entry point
├── routes/
│   ├── auth_router.py       # /login, /logout, session
│   └── analyze_router.py    # /analyze/<sector>
├── services/
│   ├── auth_service.py      # Authentications 
│   └── analyze_service.py   # Analysis flow and validations
├── lib/
│   ├── gemini.py            # genai setup and askAi with retry mechanism
│   ├── webSearch.py         # Web search for recent news of the sector 
│   └── prompts.py           # Prompt builders for Gemini
├── middleware/
│   ├── jwt_auth.py          # Cookie-based protected route logic
│   └── rate_limiter.py      # Per-user rate limiting 
└── models/
    └── userStore.py         # In-memory user data storage
```



---

##  Gemini + SerpAPI Integration

- Gemini (`google-genai`) is used to:
  - Validate sectors
  - Generate detailed markdown reports
- SerpAPI pulls recent news for the sector:
  - News title, source, thumbnail, link and other details and then feed these sources in a structured prompt to get more better result
- If SerpAPI fails → Gemini handles fallback alone

---

## API Documentation

### 1. `POST /login`

-  Description: Handles login and registration in one route. Returns a JWT token in a secure cookie.

#### Body

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

#### Success Response

```json
{
  "message": "Login successful"
}
```

### 2. `POST /logout`

- Auth Required: ✅
- Description: Logs out the user by clearing the JWT cookie.

#### Success Response

```json
{
  "message": "Logout successful"
}
```

---

### 3. `GET /analyze/{sector}`

- Auth Required: ✅ (via cookie)
- Description:
  - Validates the sector .
  - If valid: fetches recent news via SerpAPI.
  - Passes all context to Gemini and returns a detailed markdown report.

#### Example

```
GET /analyze/pharmaceuticals
```

#### Success Response (markdown content)

```json

  # Indian Pharmaceutical Sector: A Strategic Outlook (July 2025)
  ## Market Overview
  ...

```

