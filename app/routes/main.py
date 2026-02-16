"""
API routes for research brief operations
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import get_db
from app.models import ResearchBrief
from app.schemas import URLSubmission, ResearchBriefResponse
from app.services import ArticleExtractor, LLMService

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


async def process_research_brief(
    brief_id: str,
    urls: List[str],
    db: Session
) -> None:
    """
    Background task to process research brief
    
    Args:
        brief_id: ID of the research brief
        urls: List of URLs to process
        db: Database session
    """
    try:
        logger.info(f"Processing research brief {brief_id}")
        
        # Fetch and extract articles
        extractor = ArticleExtractor()
        articles = await extractor.fetch_multiple(urls)
        
        # Generate research brief using LLM
        llm_service = LLMService()
        result = await llm_service.generate_brief(articles)
        
        # Update database with result
        brief = db.query(ResearchBrief).filter(ResearchBrief.id == brief_id).first()
        if brief:
            brief.result = result
            brief.status = "completed"
            db.commit()
            logger.info(f"Successfully completed research brief {brief_id}")
        
    except Exception as e:
        logger.error(f"Error processing research brief {brief_id}: {str(e)}")
        
        # Update database with error
        brief = db.query(ResearchBrief).filter(ResearchBrief.id == brief_id).first()
        if brief:
            brief.status = "failed"
            brief.error_message = str(e)
            db.commit()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """
    Home page with URL submission form and last 5 briefs
    
    Args:
        request: FastAPI request object
        db: Database session
        
    Returns:
        HTML response with home page
    """
    # Get last 5 research briefs
    recent_briefs = (
        db.query(ResearchBrief)
        .order_by(ResearchBrief.created_at.desc())
        .limit(5)
        .all()
    )
    
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "recent_briefs": recent_briefs
        }
    )


@router.post("/submit", response_model=ResearchBriefResponse)
async def submit_urls(
    submission: URLSubmission,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit URLs for research brief generation
    
    Args:
        submission: URL submission data
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        Created research brief response
    """
    try:
        # Create database record
        brief = ResearchBrief(
            raw_urls=submission.urls,
            status="processing"
        )
        db.add(brief)
        db.commit()
        db.refresh(brief)
        
        logger.info(f"Created research brief {brief.id}")
        
        # Process in background
        # Note: We need to create a new session for background task
        from app.database import SessionLocal
        bg_db = SessionLocal()
        
        async def bg_task():
            try:
                await process_research_brief(brief.id, submission.urls, bg_db)
            finally:
                bg_db.close()
        
        background_tasks.add_task(bg_task)
        
        return ResearchBriefResponse(
            id=brief.id,
            created_at=brief.created_at,
            raw_urls=brief.raw_urls,
            result=None,
            status=brief.status,
            error_message=None
        )
        
    except Exception as e:
        logger.error(f"Error submitting URLs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/brief/{brief_id}", response_class=HTMLResponse)
async def view_brief(
    brief_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    View research brief results
    
    Args:
        brief_id: ID of the research brief
        request: FastAPI request object
        db: Database session
        
    Returns:
        HTML response with brief results
    """
    brief = db.query(ResearchBrief).filter(ResearchBrief.id == brief_id).first()
    
    if not brief:
        raise HTTPException(status_code=404, detail="Research brief not found")
    
    return templates.TemplateResponse(
        "brief.html",
        {
            "request": request,
            "brief": brief
        }
    )


@router.get("/api/brief/{brief_id}", response_model=ResearchBriefResponse)
async def get_brief_api(
    brief_id: str,
    db: Session = Depends(get_db)
):
    """
    Get research brief data via API
    
    Args:
        brief_id: ID of the research brief
        db: Database session
        
    Returns:
        Research brief response
    """
    brief = db.query(ResearchBrief).filter(ResearchBrief.id == brief_id).first()
    
    if not brief:
        raise HTTPException(status_code=404, detail="Research brief not found")
    
    return ResearchBriefResponse(
        id=brief.id,
        created_at=brief.created_at,
        raw_urls=brief.raw_urls,
        result=brief.result,
        status=brief.status,
        error_message=brief.error_message
    )
