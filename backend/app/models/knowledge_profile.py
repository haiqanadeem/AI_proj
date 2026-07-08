from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class KnowledgeProfile(Base):
    __tablename__ = "knowledge_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    topic = Column(String(100), nullable=False)
    mastery_score = Column(Float, default=0.0)
    quiz_avg = Column(Float, default=0.0)
    attempts_count = Column(Integer, default=0)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'topic', name='_user_topic_uc'),)

    # Relationships
    user = relationship("User", back_populates="knowledge_profiles")
