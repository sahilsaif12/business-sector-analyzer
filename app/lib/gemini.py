
import os
import time
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def askAi(text:str, retries: int = 3,delay=1)->str | None:
    attempts=1
    while attempts <= retries:
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=text
            )
            print("sector validation: ",response.text.strip())
            return response.text.strip()
        except Exception as e:
            
            attempt += 1
            time.sleep(delay)
            delay *= 2

            print(f"[ Error while asking AI] {e}")
    
    return None
