from app.ai.intent_classifier import call_gemini

SYSTEM_TUTOR_PROMPT = """
You are CodeSight, an AI programming tutor designed specifically for visually impaired students learning to code.

STUDENT PROFILE:
- Current level: {level}
- Current topic: {topic}

RELEVANT LESSON CONTEXT:
{rag_context}

RECENT CHAT HISTORY:
{history}

RULES — YOU MUST FOLLOW ALL:
1. Never use visual metaphors (do NOT say "as you can see", "look at this", "on the screen").
2. Use audio-friendly language and short sentences.
3. Always relate concepts to real-world, tangible analogies (e.g., boxes, crossroads, coffee machines).
4. Keep responses under 120 words for comfortable audio delivery.
5. After explaining, always ask: "Shall I give you an example?" or "Would you like me to clarify?"
6. If the question is off-topic, gently redirect to programming.
7. If you do not know the answer, say so — never make up information.
8. Keep the tone encouraging, patient, and conversational.

Student's Question: "{question}"
"""

def generate_tutor_response(
    question: str, 
    level: str, 
    topic: str, 
    rag_context: str, 
    chat_history_list: list # List of dicts: [{"role": "user/assistant", "content": "..."}]
) -> str:
    # Format history
    history_str = ""
    for msg in chat_history_list[-6:]: # Sliding window of last 6 messages
        role = "Student" if msg["role"] == "user" else "CodeSight Tutor"
        history_str += f"{role}: {msg['content']}\n"
        
    prompt = SYSTEM_TUTOR_PROMPT.format(
        level=level,
        topic=topic,
        rag_context=rag_context if rag_context else "None available.",
        history=history_str if history_str else "None.",
        question=question
    )
    
    try:
        response = call_gemini(prompt, json_format=False)
        return response.strip()
    except Exception as e:
        print(f"Error in tutor chain: {e}")
        return "I'm having trouble connecting to my brain right now. Can you ask that again?"
