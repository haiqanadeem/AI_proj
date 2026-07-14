from app.ai.gemini_client import call_gemini_json

INTENT_PROMPT = """
Classify the following voice command into exactly one intent.
The user may speak in English, Urdu, Hindi, or Roman Urdu (e.g., "registration kholo").
Return valid JSON only.

Command: "{command}"

Possible intents:
NAVIGATE_HOME, NAVIGATE_LESSONS, NAVIGATE_QUIZ, NAVIGATE_DASHBOARD, NAVIGATE_REGISTER, NAVIGATE_LOGIN,
NAVIGATE_CODE_LAB, NAVIGATE_TUTOR, NAVIGATE_SETTINGS,
OPEN_LESSON, GET_LESSON_NAME, LIST_LESSONS, NEXT_LESSON, PREVIOUS_LESSON, START_QUIZ, READ_LESSON,
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
- NAVIGATE_SETTINGS: Go to the settings page ("settings kholo", "open settings")
- GET_LESSON_NAME: Get the name of a lesson by number. Extract the number as parameter "lesson_number" (e.g. {{"lesson_number": "4"}})
- LIST_LESSONS: List all available topics or lessons ("what are the topics", "list lessons")
- OPEN_LESSON: Open a specific lesson. Extract the topic as parameter "topic" (e.g. {{"topic": "variables"}})
- NEXT_LESSON: Go to next lesson
- PREVIOUS_LESSON: Go to previous lesson
- START_QUIZ: Start a quiz. Extract topic if specified (e.g. {{"topic": "loops"}})
- READ_LESSON: Read the active lesson text
- STOP_READING: Stop reading the lesson text
- ASK_TUTOR: General programming question, concepts, or asking what happens in code (e.g. "what is a loop?", "how does python work?", "what happens if a loop runs infinitely?"). Extract the spoken question exactly as parameter "question".
- SUBMIT_CODE: Only used when the user explicitly commands to execute, submit, or evaluate the code they have already written in the editor ("mera code run karo", "submit my code", "run my code"). Do NOT use this for asking general questions about code.
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

def classify_voice_intent(command: str) -> dict:
    if not command or not command.strip():
        return {"intent": "HELP", "params": {}, "confidence": 1.0}
        
    cmd_lower = command.lower().strip()
    
    # 1. LOGOUT (Always check first)
    if any(term in cmd_lower for term in ["logout", "log out", "sign out"]):
        return {"intent": "LOGOUT", "params": {}, "confidence": 1.0}
        
    # 1.5. OPEN IN CODE LAB (Triggers SUBMIT_CODE intent to copy lesson code and open editor)
    codelab_triggers = ["open in code lab", "open in codelab", "open this in code lab", "open this in codelab", "open lesson in code lab", "open lesson in codelab"]
    if any(phrase in cmd_lower for phrase in codelab_triggers):
        return {"intent": "SUBMIT_CODE", "params": {}, "confidence": 1.0}
        
    # 1.6. SUBMIT_CODE (Local matching for executing code in the editor)
    submit_code_triggers = ["submit code", "submit my code", "run my code", "run code", "execute code", "execute my code", "evaluate code", "evaluate my code", "submit the code", "run the code"]
    if any(phrase in cmd_lower for phrase in submit_code_triggers):
        return {"intent": "SUBMIT_CODE", "params": {}, "confidence": 1.0}
        
    # 2. EVALUATE_PROGRESS (Check before question logic as it uses question words)
    progress_queries = [
        "how am i doing", "how is my progress", "evaluate my progress",
        "show me my progress", "what is my progress", "my progress",
        "show my progress", "how am i doing so far"
    ]
    if any(phrase in cmd_lower for phrase in progress_queries) or cmd_lower == "progress":
        return {"intent": "EVALUATE_PROGRESS", "params": {}, "confidence": 1.0}

    # 2.5. READ_LESSON (Local triggers to speak lesson content or written code)
    read_triggers = ["read lesson", "read the lesson", "start reading", "speak lesson", "read code", "read my code", "read the code", "what is in the editor", "read what is written in the code", "read written code", "read editor", "speak code"]
    if any(phrase in cmd_lower for phrase in read_triggers):
        return {"intent": "READ_LESSON", "params": {}, "confidence": 1.0}
        
    # 2.6. STOP_READING (Local triggers to stop speaking)
    stop_triggers = ["stop reading", "stop speaking", "stop", "shut up", "stop reader"]
    if any(phrase in cmd_lower for phrase in stop_triggers):
        return {"intent": "STOP_READING", "params": {}, "confidence": 1.0}

    # 3. OPEN_LESSON / START_QUIZ (Flexible local matching)
    open_lesson_triggers = ["open lesson", "show lesson", "start lesson", "load lesson", "go to lesson", "open chapter", "open topic", "open "]
    matched_trigger = None
    for trigger in open_lesson_triggers:
        if trigger in cmd_lower:
            matched_trigger = trigger
            break
            
    if matched_trigger:
        parts = cmd_lower.split(matched_trigger, 1)
        topic = parts[1].strip() if len(parts) > 1 else ""
        topic = topic.replace("basics", "").replace("chapter", "").strip()
        
        # Check if the extracted "topic" is actually a navigation command
        nav_keywords = {
            "home": "NAVIGATE_HOME",
            "lessons": "NAVIGATE_LESSONS",
            "lesson": "NAVIGATE_LESSONS",
            "tutor": "NAVIGATE_TUTOR",
            "code lab": "NAVIGATE_CODE_LAB", "editor": "NAVIGATE_CODE_LAB", "code editor": "NAVIGATE_CODE_LAB",
            "dashboard": "NAVIGATE_DASHBOARD",
            "settings": "NAVIGATE_SETTINGS", "setting": "NAVIGATE_SETTINGS",
            "quiz": "NAVIGATE_QUIZ", "quizzes": "NAVIGATE_QUIZ"
        }
        
        if topic in nav_keywords:
            return {"intent": nav_keywords[topic], "params": {}, "confidence": 1.0}
            
        if topic:
            return {"intent": "OPEN_LESSON", "params": {"topic": topic}, "confidence": 1.0}

    # 4. START_QUIZ / TAKE_QUIZ (Local matching)
    quiz_triggers = ["start quiz on", "take quiz on", "open quiz on", "start quiz", "take quiz", "open quiz", "start the quiz", "open the quiz"]
    matched_quiz_trigger = None
    for trigger in quiz_triggers:
        if trigger in cmd_lower:
            matched_quiz_trigger = trigger
            break
            
    if matched_quiz_trigger:
        parts = cmd_lower.split(matched_quiz_trigger, 1)
        topic = parts[1].strip() if len(parts) > 1 else ""
        # Clean up filler words like "for this lesson", "for the lesson", "this lesson"
        for filler in ["for this lesson", "for the lesson", "this lesson", "of this lesson", "of the lesson"]:
            topic = topic.replace(filler, "").strip()
        # Clean up trailing prepositions
        if topic in ["for", "of", "on", "this", "the"]:
            topic = ""
        return {"intent": "START_QUIZ", "params": {"topic": topic} if topic else {}, "confidence": 1.0}

    # 5. List lessons / topics (LIST_LESSONS) - check before question logic
    list_topics_phrases = [
        "what are the topics", "what are the lessons", 
        "list lessons", "list topics", "list all topics", "list all lessons",
        "what am i going to learn", "what am i learning", "what will i learn",
        "tell me the topics", "tell me the lessons",
        "show me the topics", "show me the lessons",
        "show all topics", "show all lessons", "read all lessons", "read all topics",
        "topics list", "lessons list", "lessons name", "topics name"
    ]
    if any(phrase in cmd_lower for phrase in list_topics_phrases) or cmd_lower in ["topics", "lessons list", "read lessons"]:
        return {"intent": "LIST_LESSONS", "params": {}, "confidence": 1.0}

    # 6. Get lesson name by number (GET_LESSON_NAME) - check before question logic
    if "lesson" in cmd_lower and any(term in cmd_lower for term in ["what is lesson", "name of lesson", "lesson number"]):
        import re
        match = re.search(r'\d+', cmd_lower)
        if match:
            return {"intent": "GET_LESSON_NAME", "params": {"lesson_number": match.group()}, "confidence": 1.0}
        
        # Check for word numbers
        word_to_num = {
            "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
            "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
            "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
            "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
            "nineteen": "19", "twenty": "20"
        }
        for word, num in word_to_num.items():
            if word in cmd_lower:
                return {"intent": "GET_LESSON_NAME", "params": {"lesson_number": num}, "confidence": 1.0}

    # 7. NAVIGATION (Only if not asking a general question)
    is_question = any(q in cmd_lower for q in ["what", "how", "why", "explain", "question", "help me with", "who", "when"]) or "?" in cmd_lower
    
    if not is_question:
        if "home" in cmd_lower:
            return {"intent": "NAVIGATE_HOME", "params": {}, "confidence": 1.0}
        if "lesson" in cmd_lower:
            return {"intent": "NAVIGATE_LESSONS", "params": {}, "confidence": 1.0}
        if "tutor" in cmd_lower:
            return {"intent": "NAVIGATE_TUTOR", "params": {}, "confidence": 1.0}
        if "code lab" in cmd_lower or "code editor" in cmd_lower or "editor" in cmd_lower:
            return {"intent": "NAVIGATE_CODE_LAB", "params": {}, "confidence": 1.0}
        if "dashboard" in cmd_lower:
            return {"intent": "NAVIGATE_DASHBOARD", "params": {}, "confidence": 1.0}
        if "setting" in cmd_lower:
            return {"intent": "NAVIGATE_SETTINGS", "params": {}, "confidence": 1.0}
        if "quiz" in cmd_lower:
            return {"intent": "NAVIGATE_QUIZ", "params": {}, "confidence": 1.0}
        if "register" in cmd_lower or "sign up" in cmd_lower or "registration" in cmd_lower:
            return {"intent": "NAVIGATE_REGISTER", "params": {}, "confidence": 1.0}
        if "login" in cmd_lower or "sign in" in cmd_lower:
            return {"intent": "NAVIGATE_LOGIN", "params": {}, "confidence": 1.0}

    prompt = INTENT_PROMPT.format(command=command)
    try:
        return call_gemini_json(prompt)
    except Exception as e:
        print(f"Failed to classify intent via Gemini Client: {e}")
        # Only fallback if we explicitly allow it, but we should raise for proper API compliance
        # since AI intent is core. But to not break the app entirely, we can do a safe fallback.
        cmd_lower = command.lower()
        if "dashboard" in cmd_lower:
            return {"intent": "NAVIGATE_DASHBOARD", "params": {}, "confidence": 0.8}
        elif "settings" in cmd_lower or "setting" in cmd_lower:
            return {"intent": "NAVIGATE_SETTINGS", "params": {}, "confidence": 0.8}
        elif "code lab" in cmd_lower or "code editor" in cmd_lower or "editor" in cmd_lower:
            return {"intent": "NAVIGATE_CODE_LAB", "params": {}, "confidence": 0.8}
        elif "tutor" in cmd_lower or "ask tutor" in cmd_lower:
            return {"intent": "NAVIGATE_TUTOR", "params": {}, "confidence": 0.8}
        elif "home" in cmd_lower:
            return {"intent": "NAVIGATE_HOME", "params": {}, "confidence": 0.8}
        elif "open" in cmd_lower:
            topic = cmd_lower.split("open")[-1].replace("lesson", "").replace("basics", "").strip()
            if not topic:
                return {"intent": "NAVIGATE_LESSONS", "params": {}, "confidence": 0.8}
            return {"intent": "OPEN_LESSON", "params": {"topic": topic}, "confidence": 0.8}
        elif "lesson" in cmd_lower or "topic" in cmd_lower:
            if "name of" in cmd_lower or "what is lesson" in cmd_lower:
                # Extract number
                import re
                match = re.search(r'\d+', cmd_lower)
                if match:
                    return {"intent": "GET_LESSON_NAME", "params": {"lesson_number": match.group()}, "confidence": 0.8}
                
                word_to_num = {
                    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
                    "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
                    "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
                    "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
                    "nineteen": "19", "twenty": "20"
                }
                for word, num in word_to_num.items():
                    if word in cmd_lower:
                        return {"intent": "GET_LESSON_NAME", "params": {"lesson_number": num}, "confidence": 0.8}
                        
            if "what are" in cmd_lower or "list" in cmd_lower or "tell me" in cmd_lower:
                return {"intent": "LIST_LESSONS", "params": {}, "confidence": 0.8}
            elif "next" in cmd_lower:
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
        elif "logout" in cmd_lower or "sign out" in cmd_lower or "log out" in cmd_lower:
            return {"intent": "LOGOUT", "params": {}, "confidence": 0.8}
        
        # If no heuristic matches, raise to bubble up error correctly instead of guessing
        raise RuntimeError(f"Intent Classification failed and no heuristic fallback matched: {e}")
