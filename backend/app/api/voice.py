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
    if not settings.OPENAI_API_KEY:
        raise HTTPException(status_code=400, detail="OpenAI API key not configured for Whisper fallback.")
        
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Write upload to temp file using safe uuid
        temp_dir = tempfile.gettempdir()
        file_ext = os.path.splitext(audio.filename)[1] or ".webm"
        temp_path = os.path.join(temp_dir, f"codesight_upload_{current_user.id}_{uuid.uuid4().hex}{file_ext}")
        
        with open(temp_path, "wb") as f:
            f.write(await audio.read())
            
        # Send to Whisper
        with open(temp_path, "rb") as audio_file:
            transcript_res = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
            
        try:
            os.remove(temp_path)
        except Exception:
            pass
            
        return {
            "transcript": transcript_res.text,
            "confidence": 0.95,
            "duration_sec": 0.0
        }
    except Exception as e:
        print(f"Whisper transcription failed: {e}")
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
