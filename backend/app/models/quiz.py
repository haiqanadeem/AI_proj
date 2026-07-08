from datetime import datetime
from sqlalchemy import Column, Integer, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    quiz_json = Column(JSON, nullable=False)      # Stores generated quiz JSON
    answers_json = Column(JSON, nullable=True)    # Stores student answers JSON
    score = Column(Float, nullable=True)          # Percentage score (0-100)
    passed = Column(Boolean, nullable=True)
    time_taken_sec = Column(Integer, nullable=True)
    attempted_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    lesson = relationship("Lesson", back_populates="quiz_attempts")
