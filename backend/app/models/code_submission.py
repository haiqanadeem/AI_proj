from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class CodeSubmission(Base):
    __tablename__ = "code_submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True)
    code = Column(Text, nullable=False)
    language = Column(String(20), default="python")
    execution_output = Column(Text, nullable=True)
    execution_errors = Column(Text, nullable=True)
    exit_code = Column(Integer, nullable=True)
    ai_analysis = Column(Text, nullable=True) # Gemini explanation of error
    execution_time_ms = Column(Integer, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="code_submissions")
    lesson = relationship("Lesson", back_populates="code_submissions")
