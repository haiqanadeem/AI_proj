from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.chat import ChatHistory
from app.models.user import User
from app.services.auth_service import get_current_user
from app.ai.rag_retriever import retrieve_context
from app.ai.tutor_chain import generate_tutor_response

router = APIRouter(prefix="/tutor", tags=["tutor"])

class LessonContext(BaseModel):
    lesson_id: int
    topic: str

class ChatRequest(BaseModel):
    message: str
    session_id: str
    lesson_context: Optional[LessonContext] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    tokens_used: int
    rag_sources: list

@router.post("/chat", response_model=ChatResponse)
def tutor_chat(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        topic = req.lesson_context.topic if req.lesson_context else None
        
        # 1. Retrieve RAG Context
        rag_context, metadata_list = retrieve_context(
            question=req.message,
            difficulty=current_user.level,
            n_results=3
        )
        
        # 2. Get past chat history from database
        history_records = db.query(ChatHistory).filter(
            ChatHistory.user_id == current_user.id,
            ChatHistory.session_id == req.session_id
        ).order_by(ChatHistory.created_at.asc()).all()
        
        history_list = [{"role": rec.role, "content": rec.content} for rec in history_records]
        
        # 3. Generate response using AI
        ai_response = generate_tutor_response(
            question=req.message,
            level=current_user.level,
            topic=topic or "General Python Programming",
            rag_context=rag_context,
            chat_history_list=history_list
        )
        
        # 4. Save both messages to database
        user_msg = ChatHistory(
            user_id=current_user.id,
            session_id=req.session_id,
            role="user",
            content=req.message
        )
        db.add(user_msg)
        
        assistant_msg = ChatHistory(
            user_id=current_user.id,
            session_id=req.session_id,
            role="assistant",
            content=ai_response,
            retrieved_chunks=[meta for meta in metadata_list] if metadata_list else []
        )
        db.add(assistant_msg)
        db.commit()
        
        # Return format
        sources = [meta.get("lesson_title", "Unknown Lesson") for meta in metadata_list] if metadata_list else []
        return {
            "response": ai_response,
            "session_id": req.session_id,
            "tokens_used": len(req.message.split()) + len(ai_response.split()), # simple estimation
            "rag_sources": sources
        }
    except Exception as e:
        print(f"Error in tutor chat api: {e}")
        raise HTTPException(status_code=500, detail=str(e))
