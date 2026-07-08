import json
from app.ai.intent_classifier import call_gemini

CODE_ANALYSIS_PROMPT = """
You are a Python code reviewer helper for beginner programming students who are visually impaired and get feedback through audio.

STUDENT CODE:
{code}

EXECUTION ERROR (if any):
{error}

TASK:
1. Detect any errors (syntax, logic, runtime).
2. Explain the error in very simple terms (max 2 sentences).
3. Provide the exact corrected line of code.
4. "spoken_summary" MUST be optimized for Text-to-Speech: do not use special symbols like braces, parens, brackets, or backticks. Speak code out loud naturally (e.g. "for i in range of 5, colon" instead of "for i in range(5):").

Return ONLY valid JSON matching this schema:
{{
  "has_errors": {has_errors},
  "errors": [
    {{
      "type": "SyntaxError" | "LogicError" | "RuntimeError",
      "description": "simple error explanation",
      "line": 1,
      "fix": "corrected code line"
    }}
  ],
  "positive_feedback": "what they did well (e.g. good indentation, good variable naming)",
  "spoken_summary": "spoken summary designed for blind student text-to-speech audio feedback"
}}
"""

def analyze_student_code(code: str, execution_error: str = None) -> dict:
    has_errors = "true" if execution_error else "false"
    prompt = CODE_ANALYSIS_PROMPT.format(code=code, error=execution_error or "None", has_errors=has_errors)
    
    try:
        raw_response = call_gemini(prompt)
        clean_json = raw_response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
        clean_json = clean_json.strip()
        
        parsed = json.loads(clean_json)
        return parsed
    except Exception as e:
        print(f"Failed to analyze code with Gemini: {e}")
        # Fallback analysis
        if execution_error:
            return {
                "has_errors": True,
                "errors": [
                    {
                        "type": "Error",
                        "description": execution_error,
                        "line": 1,
                        "fix": "Please check your code syntax."
                    }
                ],
                "positive_feedback": "Nice attempt at writing code!",
                "spoken_summary": f"Your code failed to run with the error: {execution_error}. Please double check the syntax."
            }
        else:
            return {
                "has_errors": False,
                "errors": [],
                "positive_feedback": "Your code executes successfully with zero errors. Excellent job!",
                "spoken_summary": "Your code executed successfully with no errors. Good work!"
            }
