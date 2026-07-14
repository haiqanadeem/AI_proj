import json
import google.generativeai as genai
from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

# Configure Gemini globally
if settings.GOOGLE_API_KEY:
    genai.configure(api_key=settings.GOOGLE_API_KEY)
    try:
        print("--- AVAILABLE MODELS FOR YOUR API KEY ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
        print("-----------------------------------------")
    except Exception as e:
        print(f"Failed to list models: {e}")

# Define robust retry logic: wait 2^x * 1 second between each retry, up to 4 seconds, max 3 attempts
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4))
def call_gemini(prompt: str, expect_json: bool = True, model_name: str = "gemini-flash-latest") -> str:
    """
    Robust centralized client to call the Gemini API.
    Handles retries, exponential backoff, and JSON structuring.
    """
    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    model = genai.GenerativeModel(model_name)
    
    # Configure safety settings to avoid blocked RAG content unnecessarily
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    config = GenerationConfig()
    if expect_json:
        config.response_mime_type = "application/json"
        
    try:
        response = model.generate_content(
            prompt,
            generation_config=config,
            safety_settings=safety_settings
        )
        return response.text
    except Exception as e:
        print(f"Gemini API Exception: {e}")
        raise e

def call_gemini_json(prompt: str, model_name: str = "gemini-flash-latest") -> dict:
    """
    Calls Gemini API and safely parses the JSON response.
    """
    response_text = call_gemini(prompt, expect_json=True, model_name=model_name)
    try:
        # Gemini sometimes wraps JSON in markdown blocks even with mime_type set
        clean_json = response_text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()
        
        return json.loads(clean_json)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e} | Raw Response: {response_text}")
        raise ValueError(f"Failed to parse JSON from Gemini: {e}")
