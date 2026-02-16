"""
Database models for Research Brief application
"""
from sqlalchemy import Column, String, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class ResearchBrief(Base):
    """
    ResearchBrief model for storing research brief data
    
    Attributes:
        id: UUID primary key
        created_at: Timestamp of creation
        raw_urls: JSON array of submitted URLs
        result: JSON object containing the structured research brief
        status: Current status (processing/completed/failed)
        error_message: Error message if status is failed
    """
    __tablename__ = "research_briefs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    raw_urls = Column(JSON, nullable=False)
    result = Column(JSON, nullable=True)
    status = Column(String(20), nullable=False, default="processing")
    error_message = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<ResearchBrief(id={self.id}, status={self.status})>"
