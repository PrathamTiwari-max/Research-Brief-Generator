"""
Routes package initialization
"""
from app.routes.main import router as main_router
from app.routes.health import router as health_router

__all__ = ["main_router", "health_router"]
