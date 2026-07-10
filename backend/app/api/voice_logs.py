from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.database.connection import get_db
from app.models.user import User
from app.models.voice_log import VoiceLog
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/voice-logs", tags=["voice_logs"])

class VoiceLogCreate(BaseModel):
    command: str
    intent_detected: Optional[str] = None
    confidence_score: Optional[float] = None
    execution_time_ms: Optional[int] = None

class VoiceLogResponse(BaseModel):
    id: int
    user_id: int
    command: str
    intent_detected: Optional[str]
    confidence_score: Optional[float]
    execution_time_ms: Optional[int]
    timestamp: datetime

@router.post("", response_model=VoiceLogResponse, status_code=201)
def create_voice_log(
    req: VoiceLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        log_entry = VoiceLog(
            user_id=current_user.id,
            raw_transcript=req.command,
            classified_intent=req.intent_detected,
            confidence=req.confidence_score,
            intent_params={"execution_time_ms": req.execution_time_ms} if req.execution_time_ms else {}
        )
        db.add(log_entry)
        db.commit()
        db.refresh(log_entry)
        
        return VoiceLogResponse(
            id=log_entry.id,
            user_id=log_entry.user_id,
            command=log_entry.raw_transcript,
            intent_detected=log_entry.classified_intent,
            confidence_score=log_entry.confidence,
            execution_time_ms=log_entry.intent_params.get("execution_time_ms") if log_entry.intent_params else None,
            timestamp=log_entry.created_at
        )
    except Exception as e:
        print(f"Failed to create voice log: {e}")
        raise HTTPException(status_code=500, detail="Failed to save voice log.")

@router.get("", response_model=List[VoiceLogResponse])
def get_user_voice_logs(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(VoiceLog).filter(VoiceLog.user_id == current_user.id).order_by(VoiceLog.created_at.desc()).limit(limit).all()
    return [
        VoiceLogResponse(
            id=l.id,
            user_id=l.user_id,
            command=l.raw_transcript,
            intent_detected=l.classified_intent,
            confidence_score=l.confidence,
            execution_time_ms=l.intent_params.get("execution_time_ms") if l.intent_params else None,
            timestamp=l.created_at
        ) for l in logs
    ]
