from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from app.models.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    topic = Column(String(100), nullable=False)
    difficulty = Column(String(20), nullable=False) # beginner | intermediate | advanced
    content = Column(Text, nullable=False)
    code_example = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, default=15)
    vector_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    quiz_json = Column(JSON, nullable=True)

    # Relationships
    progress_records = relationship("Progress", back_populates="lesson")
    quiz_attempts = relationship("QuizAttempt", back_populates="lesson")
    code_submissions = relationship("CodeSubmission", back_populates="lesson")
