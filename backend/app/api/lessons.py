from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.lesson import Lesson
from app.models.progress import Progress
from app.models.user import User
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/lessons", tags=["lessons"])

class ProgressResponse(BaseModel):
    status: str
    completion_pct: int
    class Config:
        orm_mode = True
        from_attributes = True

class LessonBrief(BaseModel):
    id: int
    title: str
    slug: str
    topic: str
    difficulty: str
    order_index: int
    estimated_minutes: int
    class Config:
        orm_mode = True
        from_attributes = True

class LessonListResponse(BaseModel):
    lessons: List[LessonBrief]
    total: int

class LessonDetailResponse(BaseModel):
    id: int
    title: str
    slug: str
    topic: str
    difficulty: str
    content: str
    code_example: Optional[str]
    order_index: int
    estimated_minutes: int
    user_progress: Optional[ProgressResponse] = None
    next_lesson_id: Optional[int] = None
    prev_lesson_id: Optional[int] = None
    class Config:
        orm_mode = True
        from_attributes = True

@router.get("", response_model=LessonListResponse)
def get_lessons(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)
    if difficulty:
        query = query.filter(Lesson.difficulty == difficulty)
    if topic:
        query = query.filter(Lesson.topic == topic)
        
    lessons = query.order_by(Lesson.order_index).all()
    return {
        "lessons": lessons,
        "total": len(lessons)
    }

@router.get("/{lesson_id}", response_model=LessonDetailResponse)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    # Get user progress if logged in
    user_progress = None
    if current_user:
        progress = db.query(Progress).filter(
            Progress.user_id == current_user.id,
            Progress.lesson_id == lesson.id
        ).first()
        if not progress:
            # Create a "not started" entry
            progress = Progress(
                user_id=current_user.id,
                lesson_id=lesson.id,
                status="not_started",
                completion_pct=0,
                started_at=datetime.utcnow()
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)
        user_progress = progress

    # Get next and previous lesson IDs
    next_lesson = db.query(Lesson).filter(Lesson.order_index > lesson.order_index).order_by(Lesson.order_index.asc()).first()
    prev_lesson = db.query(Lesson).filter(Lesson.order_index < lesson.order_index).order_by(Lesson.order_index.desc()).first()
        
    return {
        "id": lesson.id,
        "title": lesson.title,
        "slug": lesson.slug,
        "topic": lesson.topic,
        "difficulty": lesson.difficulty,
        "content": lesson.content,
        "code_example": lesson.code_example,
        "order_index": lesson.order_index,
        "estimated_minutes": lesson.estimated_minutes,
        "user_progress": user_progress,
        "next_lesson_id": next_lesson.id if next_lesson else None,
        "prev_lesson_id": prev_lesson.id if prev_lesson else None
    }
