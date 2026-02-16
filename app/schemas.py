"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
import re


class URLSubmission(BaseModel):
    """Schema for URL submission"""
    urls: List[str] = Field(..., min_length=1, max_length=10)
    
    @field_validator('urls')
    @classmethod
    def validate_urls(cls, v: List[str]) -> List[str]:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        for url in v:
            url = url.strip()
            if not url_pattern.match(url):
                raise ValueError(f"Invalid URL format: {url}")
        
        return [url.strip() for url in v]


class KeyPoint(BaseModel):
    """Schema for a key point"""
    point: str
    source_url: str
    source_snippet: str


class ConflictingClaim(BaseModel):
    """Schema for a conflicting claim"""
    claim: str
    sources: List[str]


class ResearchBriefResult(BaseModel):
    """Schema for research brief result"""
    summary: str
    key_points: List[KeyPoint]
    conflicting_claims: List[ConflictingClaim]
    verification_checklist: List[str]


class ResearchBriefResponse(BaseModel):
    """Schema for research brief response"""
    id: str
    created_at: datetime
    raw_urls: List[str]
    result: Optional[ResearchBriefResult]
    status: str
    error_message: Optional[str]
    
    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    """Schema for health check response"""
    backend: str
    database: str
    llm: str
