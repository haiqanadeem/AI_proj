import json
import urllib.request
import urllib.error
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings

# ────────────────────────────────────────────────────────────────────
# Dual-Provider LLM Client
# Priority: OpenRouter (qwen/qwen-2.5-72b-instruct) → Gemini fallback
# Provider is checked ONCE at startup, cached for all subsequent calls.
# ────────────────────────────────────────────────────────────────────

_active_provider = None  # "openrouter" | "gemini" | None


def _test_openrouter() -> bool:
    """Test OpenRouter connectivity at startup."""
    if not settings.OPENROUTER_API_KEY:
        return False
    try:
        payload = json.dumps({
            "model": settings.OPENROUTER_MODEL,
            "messages": [{"role": "user", "content": "ping"}],
            "max_tokens": 5
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
                "X-Title": "CodeSight AI"
            }
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            json.loads(resp.read().decode())
        return True
    except Exception as e:
        print(f"OpenRouter startup test failed: {e}")
        return False


def _test_gemini() -> bool:
    """Test Gemini connectivity at startup."""
    if not settings.GOOGLE_API_KEY:
        return False
    try:
        import google.generativeai as genai
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-flash-latest")
        model.generate_content("ping")
        return True
    except Exception as e:
        print(f"Gemini startup test failed: {e}")
        return False


def initialize_llm_provider():
    """Called once at startup. Tests providers in priority order and caches the result."""
    global _active_provider

    print("\n🔍 Checking LLM providers...")

    # Priority 1: OpenRouter
    if _test_openrouter():
        _active_provider = "openrouter"
        print(f"✅ Active LLM Provider: OpenRouter ({settings.OPENROUTER_MODEL})")
        return

    # Priority 2: Gemini
    if _test_gemini():
        _active_provider = "gemini"
        print("✅ Active LLM Provider: Google Gemini (gemini-flash-latest)")
        return

    _active_provider == None
    print("❌ WARNING: No LLM provider is available! AI features will not work.")


# Run provider check on module import (happens once at server startup)
initialize_llm_provider()


# ────────────────────────────────────────────────────────────────────
# OpenRouter call implementation
# ────────────────────────────────────────────────────────────────────

def _call_openrouter(prompt: str, expect_json: bool = True) -> str:
    """Call OpenRouter API (OpenAI-compatible)."""
    messages = [{"role": "user", "content": prompt}]

    body = {
        "model": settings.OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 4096,
    }

    if expect_json:
        body["response_format"] = {"type": "json_object"}

    payload = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "CodeSight AI"
        }
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode())

    return data["choices"][0]["message"]["content"]


# ────────────────────────────────────────────────────────────────────
# Gemini call implementation
# ────────────────────────────────────────────────────────────────────

def _call_gemini(prompt: str, expect_json: bool = True, model_name: str = "gemini-flash-latest") -> str:
    """Call Google Gemini API directly."""
    import google.generativeai as genai
    from google.generativeai.types import GenerationConfig, HarmCategory, HarmBlockThreshold

    if not settings.GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not configured.")

    genai.configure(api_key=settings.GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)

    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

    config = GenerationConfig()
    if expect_json:
        config.response_mime_type = "application/json"

    response = model.generate_content(
        prompt,
        generation_config=config,
        safety_settings=safety_settings
    )
    return response.text


# ────────────────────────────────────────────────────────────────────
# Public API (same interface as before — drop-in replacement)
# ────────────────────────────────────────────────────────────────────

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=4))
def call_gemini(prompt: str, expect_json: bool = True, model_name: str = "gemini-flash-latest") -> str:
    """
    Unified LLM client. Routes to the active provider (checked once at startup).
    Handles retries, exponential backoff, and JSON structuring.
    """
    if _active_provider == "openrouter":
        try:
            return _call_openrouter(prompt, expect_json)
        except Exception as e:
            print(f"OpenRouter API Exception: {e}")
            raise e
    elif _active_provider == "gemini":
        try:
            return _call_gemini(prompt, expect_json, model_name)
        except Exception as e:
            print(f"Gemini API Exception: {e}")
            raise e
    else:
        raise ValueError("No LLM provider is available. Check your API keys in .env")


def call_gemini_json(prompt: str, model_name: str = "gemini-flash-latest") -> dict:
    """
    Calls the active LLM provider and safely parses the JSON response.
    """
    response_text = call_gemini(prompt, expect_json=True, model_name=model_name)
    try:
        # LLMs sometimes wrap JSON in markdown blocks
        clean_json = response_text.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()

        return json.loads(clean_json)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e} | Raw Response: {response_text}")
        raise ValueError(f"Failed to parse JSON from LLM: {e}")
