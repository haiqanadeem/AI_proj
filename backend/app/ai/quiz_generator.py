import json
from app.ai.intent_classifier import call_gemini

QUIZ_PROMPT = """
Generate a programming quiz based on the following:
- Topic: {topic}
- Difficulty: {difficulty}
- Student Level: {level}

Create exactly 5 questions matching this distribution:
- 3 multiple-choice questions (MCQs)
- 1 code completion question (fill-in-the-blank)
- 1 debugging question

CRITICAL CONSTRAINTS:
1. Every question must work well when read aloud.
2. It must be fully answerable without seeing code visually (blind students use text-to-speech). So describe code logic in words or keep code snippets extremely simple and short, using plain spoken representation.
3. Multiple-choice options must always start with letter prefix followed by a colon (e.g. "A: ...", "B: ...", "C: ...", "D: ...").
4. "correct_answer" must be exactly "A", "B", "C", or "D".
5. Provide a short explanation (1-2 sentences) explaining why it's correct.

Return ONLY valid JSON matching this schema exactly:
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "id": 1,
      "type": "mcq" | "code_completion" | "debug",
      "question": "string describing the question",
      "options": ["A: option text", "B: option text", "C: option text", "D: option text"],
      "correct_answer": "A" | "B" | "C" | "D",
      "explanation": "string explanation"
    }}
  ]
}}
"""

def generate_quiz_for_topic(topic: str, difficulty: str, level: str) -> dict:
    prompt = QUIZ_PROMPT.format(topic=topic, difficulty=difficulty, level=level)
    try:
        raw_response = call_gemini(prompt)
        # Clean any markdown code blocks
        clean_json = raw_response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()
        
        parsed = json.loads(clean_json)
        return parsed
    except Exception as e:
        print(f"Failed to generate AI quiz: {e}")
        # Return fallback static quiz if LLM fails
        return {
            "topic": topic,
            "difficulty": difficulty,
            "questions": [
                {
                    "id": 1,
                    "type": "mcq",
                    "question": f"Which of the following is true about {topic} in Python?",
                    "options": [
                        "A: It is a fundamental programming concept",
                        "B: Python does not support it",
                        "C: It can only be used in print statements",
                        "D: It is deprecated"
                    ],
                    "correct_answer": "A",
                    "explanation": f"{topic} is a core building block of Python programming."
                },
                {
                    "id": 2,
                    "type": "mcq",
                    "question": "What is the primary benefit of clean code structure?",
                    "options": [
                        "A: Runs 100 times faster",
                        "B: Code is easier to read and maintain",
                        "C: Computer saves electricity",
                        "D: Prevents internet from breaking"
                    ],
                    "correct_answer": "B",
                    "explanation": "Readable code helps other developers and makes debugging much simpler."
                },
                {
                    "id": 3,
                    "type": "mcq",
                    "question": "In Python, which character is used to start a comment?",
                    "options": [
                        "A: Forward slash",
                        "B: Dollar sign",
                        "C: Hash symbol",
                        "D: Ampersand"
                    ],
                    "correct_answer": "C",
                    "explanation": "Python comments start with the hash (#) symbol."
                },
                {
                    "id": 4,
                    "type": "code_completion",
                    "question": "Fill in the blank: print underscore 'Hello World' underscore. What is used to output text?",
                    "options": [
                        "A: display",
                        "B: input",
                        "C: print",
                        "D: show"
                    ],
                    "correct_answer": "C",
                    "explanation": "The print function outputs text to the screen."
                },
                {
                    "id": 5,
                    "type": "debug",
                    "question": "What is wrong with this code: print Hello without quotes?",
                    "options": [
                        "A: print must be capitalized",
                        "B: Hello must be wrapped in quotation marks",
                        "C: missing semicolon at end",
                        "D: nothing is wrong"
                    ],
                    "correct_answer": "B",
                    "explanation": "Strings in Python must be enclosed in quotes."
                }
            ]
        }
