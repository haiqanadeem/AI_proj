import os
import tempfile
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.config import settings
from app.models.voice_log import VoiceLog
from app.services.auth_service import get_current_user, get_optional_current_user
from app.models.user import User
from app.ai.intent_classifier import classify_voice_intent
from typing import Optional

# Initialize WhisperModel once globally (saves 5-10s per request)
whisper_model = None

def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            # Using base model for good balance of speed and accuracy on CPU
            # compute_type="int8" reduces memory usage with almost no quality loss
            whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
            print("🚀 WhisperModel pre-loaded successfully in background!")
        except Exception as e:
            print(f"Error loading WhisperModel: {e}")
            raise e
    return whisper_model

# Pre-load model in a background thread so it doesn't block server startup
import threading
threading.Thread(target=get_whisper_model, daemon=True).start()

router = APIRouter(tags=["voice"])

class IntentRequest(BaseModel):
    transcript: str

class IntentResponse(BaseModel):
    intent: str
    params: dict
    confidence: float
    raw_command: str

@router.post("/voice/transcribe")
async def transcribe_audio(
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        model = get_whisper_model()
        
        # Write upload to temp file using safe uuid
        temp_dir = tempfile.gettempdir()
        file_ext = os.path.splitext(audio.filename)[1] or ".m4a"
        temp_path = os.path.join(temp_dir, f"codesight_upload_{current_user.id}_{uuid.uuid4().hex}{file_ext}")
        
        with open(temp_path, "wb") as f:
            f.write(await audio.read())
            
        # Transcribe with faster-whisper
        segments, info = model.transcribe(temp_path, beam_size=5)
        
        transcript_text = ""
        for segment in segments:
            transcript_text += segment.text + " "
            
        try:
            os.remove(temp_path)
        except Exception:
            pass
            
        return {
            "transcript": transcript_text.strip(),
            "confidence": 0.95,
            "duration_sec": 0.0
        }
    except Exception as e:
        print(f"Faster-Whisper transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription error: {str(e)}")

@router.post("/ai/classify-intent", response_model=IntentResponse)
def classify_intent(
    req: IntentRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user)
):
    user_id = current_user.id if current_user else None
    try:
        result = classify_voice_intent(req.transcript)
        
        # If intent is OPEN_LESSON or START_QUIZ, try to resolve the topic to a lesson_id
        if result.get("intent") in ["OPEN_LESSON", "START_QUIZ"] and result.get("params", {}).get("topic"):
            from app.models.lesson import Lesson
            topic_str = str(result["params"]["topic"]).lower().strip()
            lessons = db.query(Lesson).all()
            
            best_match = None
            max_score = 0
            
            # Map word numbers to digits
            word_to_num = {
                "one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
                "six": "6", "seven": "7", "eight": "8", "nine": "9", "ten": "10",
                "eleven": "11", "twelve": "12", "thirteen": "13", "fourteen": "14",
                "fifteen": "15", "sixteen": "16", "seventeen": "17", "eighteen": "18",
                "nineteen": "19", "twenty": "20", "twenty one": "21", "twenty two": "22"
            }
            
            # Check if the user asked by number
            lesson_idx = None
            if topic_str.isdigit():
                lesson_idx = int(topic_str)
            elif topic_str in word_to_num:
                lesson_idx = int(word_to_num[topic_str])
            elif topic_str.replace("lesson", "").strip().isdigit():
                lesson_idx = int(topic_str.replace("lesson", "").strip())
                
            if lesson_idx is not None:
                best_match = db.query(Lesson).filter(Lesson.order_index == lesson_idx).first()
            
            if not best_match:
                topic_words = set(topic_str.replace("-", " ").replace("_", " ").split())
                stop_words = {"the", "a", "an", "lesson", "open", "chapter", "and", "or", "to", "of", "in"}
                topic_words = topic_words - stop_words
                
                for l in lessons:
                    title_lower = l.title.lower()
                    topic_lower = l.topic.lower()
                    
                    if topic_str in title_lower or topic_str in topic_lower:
                        best_match = l
                        break
                        
                    score = 0
                    title_words = set(title_lower.replace("-", " ").replace("_", " ").split())
                    topic_f_words = set(topic_lower.replace("-", " ").replace("_", " ").split())
                    
                    score += len(topic_words & title_words)
                    score += len(topic_words & topic_f_words)
                    
                    if score > max_score:
                        max_score = score
                        best_match = l
                        
            if best_match:
                result["params"]["lesson_id"] = best_match.id

        # Log to voice_logs table
        voice_log = VoiceLog(
            user_id=user_id,
            raw_transcript=req.transcript,
            classified_intent=result.get("intent"),
            intent_params=result.get("params"),
            confidence=result.get("confidence", 0.0),
            success=True
        )
        db.add(voice_log)
        db.commit()
        
        return {
            "intent": result.get("intent"),
            "params": result.get("params", {}),
            "confidence": result.get("confidence", 1.0),
            "raw_command": req.transcript
        }
    except Exception as e:
        # Log failure
        voice_log = VoiceLog(
            user_id=user_id,
            raw_transcript=req.transcript,
            classified_intent="HELP",
            intent_params={},
            confidence=0.0,
            success=False,
            error_message=str(e)
        )
        db.add(voice_log)
        db.commit()
        
        # Return graceful fallback instead of raising 500 error
        return {
            "intent": "HELP",
            "params": {},
            "confidence": 0.0,
            "raw_command": req.transcript
        }
