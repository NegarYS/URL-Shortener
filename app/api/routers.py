"""
API router for version 1 of URL Shortener.
"""

from fastapi import APIRouter

from app.api.controllers import links

# Create router for API v1
router = APIRouter(prefix="/api/v1")

# Include link endpoints
router.include_router(links.router, tags=["links"])

# Health check
@router.get("/health")
def v1_health_check():
    """Health check for API v1."""
    return {
        "status": "healthy",
        "version": "v1",
        "service": "url-shortener"
    }