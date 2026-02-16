"""
Health check and status routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging

from app.database import get_db
from app.schemas import HealthCheckResponse
from app.services import LLMService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/status", response_model=HealthCheckResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    
    Returns:
        Health status of backend, database, and LLM
    """
    # Backend is always ok if we reach here
    backend_status = "ok"
    
    # Check database connection
    database_status = "ok"
    try:
        db.execute(text("SELECT 1"))
        logger.info("Database connection check: OK")
    except Exception as e:
        database_status = "error"
        logger.error(f"Database connection check failed: {str(e)}")
    
    # Check LLM API key
    llm_status = "ok"
    try:
        llm_service = LLMService()
        if not llm_service.validate_api_key():
            llm_status = "error"
            logger.error("LLM API key validation failed")
        else:
            logger.info("LLM API key validation: OK")
    except Exception as e:
        llm_status = "error"
        logger.error(f"LLM validation failed: {str(e)}")
    
    return HealthCheckResponse(
        backend=backend_status,
        database=database_status,
        llm=llm_status
    )
