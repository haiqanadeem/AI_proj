import json
import urllib.request
import urllib.error
from app.config import settings

INTENT_PROMPT = """
Classify the following voice command into exactly one intent.
The user may speak in English, Urdu, Hindi, or Roman Urdu (e.g., "registration kholo", "mera naam hafiz likho").
Return valid JSON only.

Command: "{command}"

Possible intents:
NAVIGATE_HOME, NAVIGATE_LESSONS, NAVIGATE_QUIZ, NAVIGATE_DASHBOARD, NAVIGATE_REGISTER, NAVIGATE_LOGIN,
NAVIGATE_CODE_LAB, NAVIGATE_TUTOR,
OPEN_LESSON, NEXT_LESSON, PREVIOUS_LESSON, START_QUIZ, READ_LESSON,
STOP_READING, ASK_TUTOR, SUBMIT_CODE, EVALUATE_PROGRESS, LOGOUT, HELP, REPEAT_LAST, DICTATE_TEXT, FILL_FIELD, SUBMIT_FORM

Intent explanations:
- NAVIGATE_HOME: Go to home screen ("home pe jao")
- NAVIGATE_REGISTER: Go to the registration page ("registration kholo", "sign up kholo")
- NAVIGATE_LOGIN: Go to the login page ("login kholo", "sign in page")
- NAVIGATE_LESSONS: Go to lesson library
- NAVIGATE_QUIZ: Go to quiz page
- NAVIGATE_DASHBOARD: Go to student progress dashboard
- NAVIGATE_CODE_LAB: Go to the code lab / code editor ("code lab kholo", "open code editor")
- NAVIGATE_TUTOR: Go to the AI tutor chat page ("tutor kholo", "open tutor")
- OPEN_LESSON: Open a specific lesson. Extract the topic as parameter "topic" (e.g. {{"topic": "variables"}})
- NEXT_LESSON: Go to next lesson
- PREVIOUS_LESSON: Go to previous lesson
- START_QUIZ: Start a quiz. Extract topic if specified (e.g. {{"topic": "loops"}})
- READ_LESSON: Read the active lesson text
- STOP_READING: Stop reading the lesson text
- ASK_TUTOR: General programming question. Extract the question as parameter "question"
- SUBMIT_CODE: Evaluate/run the student's code ("mera code run karo")
- EVALUATE_PROGRESS: Spoken progress summary
- LOGOUT: User wants to logout
- HELP: Command help menu
- REPEAT_LAST: Repeat the last spoken text
- DICTATE_TEXT: User wants to type text into a generic field. Extract exact text as "text" parameter.
- FILL_FIELD: User wants to fill a specific form field (like name, email, password, username). Extract "field" (the semantic name of the field) and "value" (what to fill in). Example: "mera naam hafiz likho" -> {{"field": "name", "value": "hafiz"}}
- SUBMIT_FORM: User wants to submit the current form or register/login ("register kar do", "submit the form")

Response format MUST be a single JSON object matching this schema:
{{
  "intent": "INTENT_NAME",
  "params": {{}},
  "confidence": 0.0-1.0
}}
"""

def call_gemini(prompt: str, json_format: bool = True) -> str:
    if not settings.GOOGLE_API_KEY:
        raise ValueError("Google API key is not configured.")
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {}
    }
    
    if json_format:
        data["generationConfig"]["responseMimeType"] = "application/json"
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"Gemini HTTP Error: {e.code} - {error_body}")
        raise e
    except Exception as e:
        print(f"Gemini Connection Error: {e}")
        raise e

def classify_voice_intent(command: str) -> dict:
    if not command or not command.strip():
        return {"intent": "HELP", "params": {}, "confidence": 1.0}
        
    prompt = INTENT_PROMPT.format(command=command)
    try:
        raw_response = call_gemini(prompt)
        parsed = json.loads(raw_response.strip())
        return parsed
    except Exception as e:
        print(f"Failed to classify intent: {e}")
        # Graceful fallback logic
        cmd_lower = command.lower()
        if "open" in cmd_lower:
            topic = cmd_lower.split("open")[-1].replace("lesson", "").replace("basics", "").strip()
            return {"intent": "OPEN_LESSON", "params": {"topic": topic}, "confidence": 0.8}
        elif "home" in cmd_lower:
            return {"intent": "NAVIGATE_HOME", "params": {}, "confidence": 0.8}
        elif "lesson" in cmd_lower:
            if "next" in cmd_lower:
                return {"intent": "NEXT_LESSON", "params": {}, "confidence": 0.8}
            elif "previous" in cmd_lower or "back" in cmd_lower:
                return {"intent": "PREVIOUS_LESSON", "params": {}, "confidence": 0.8}
            elif "read" in cmd_lower:
                return {"intent": "READ_LESSON", "params": {}, "confidence": 0.8}
            else:
                return {"intent": "NAVIGATE_LESSONS", "params": {}, "confidence": 0.7}
        elif "quiz" in cmd_lower:
            return {"intent": "START_QUIZ", "params": {}, "confidence": 0.8}
        elif "what is" in cmd_lower or "explain" in cmd_lower or "how to" in cmd_lower or "?" in cmd_lower:
            return {"intent": "ASK_TUTOR", "params": {"question": command}, "confidence": 0.8}
        elif "submit" in cmd_lower or "run" in cmd_lower or "evaluate" in cmd_lower:
            return {"intent": "SUBMIT_CODE", "params": {}, "confidence": 0.8}
        elif "progress" in cmd_lower or "score" in cmd_lower:
            return {"intent": "EVALUATE_PROGRESS", "params": {}, "confidence": 0.8}
        elif "code lab" in cmd_lower or "code editor" in cmd_lower or "editor" in cmd_lower:
            return {"intent": "NAVIGATE_CODE_LAB", "params": {}, "confidence": 0.8}
        elif "tutor" in cmd_lower or "ask tutor" in cmd_lower:
            return {"intent": "NAVIGATE_TUTOR", "params": {}, "confidence": 0.8}
        elif "type " in cmd_lower or "write " in cmd_lower or "dictate " in cmd_lower or "enter " in cmd_lower:
            for keyword in ["type ", "write ", "dictate ", "enter "]:
                if keyword in cmd_lower:
                    text = cmd_lower.split(keyword, 1)[1].strip()
                    return {"intent": "DICTATE_TEXT", "params": {"text": text}, "confidence": 0.8}
        elif "register" in cmd_lower or "registration" in cmd_lower or "sign up" in cmd_lower:
            if "submit" in cmd_lower or "kar do" in cmd_lower:
                return {"intent": "SUBMIT_FORM", "params": {}, "confidence": 0.8}
            return {"intent": "NAVIGATE_REGISTER", "params": {}, "confidence": 0.8}
        elif "login" in cmd_lower or "sign in" in cmd_lower:
            if "submit" in cmd_lower or "kar do" in cmd_lower:
                return {"intent": "SUBMIT_FORM", "params": {}, "confidence": 0.8}
            return {"intent": "NAVIGATE_LOGIN", "params": {}, "confidence": 0.8}
        elif "naam" in cmd_lower or "name" in cmd_lower:
            val = cmd_lower.replace("mera", "").replace("naam", "").replace("name", "").replace("likho", "").replace("rakho", "").replace("set", "").replace("karo", "").strip()
            return {"intent": "FILL_FIELD", "params": {"field": "name", "value": val}, "confidence": 0.8}
        elif "email" in cmd_lower:
            val = cmd_lower.replace("mera", "").replace("email", "").replace("likho", "").replace("rakho", "").replace("set", "").replace("karo", "").replace(" at ", "@").replace(" dot ", ".").strip()
            return {"intent": "FILL_FIELD", "params": {"field": "email", "value": val}, "confidence": 0.8}
        elif "password" in cmd_lower:
            val = cmd_lower.replace("mera", "").replace("password", "").replace("likho", "").replace("rakho", "").replace("set", "").replace("karo", "").strip()
            return {"intent": "FILL_FIELD", "params": {"field": "password", "value": val}, "confidence": 0.8}
        elif "submit" in cmd_lower or "kar do" in cmd_lower or "done" in cmd_lower:
            return {"intent": "SUBMIT_FORM", "params": {}, "confidence": 0.8}
            
        return {"intent": "HELP", "params": {}, "confidence": 0.5}
