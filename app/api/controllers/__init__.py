"""
Controllers package for URL Shortener API.
Exposes the main router for API endpoints.
"""

from app.api.controllers.links import router as links_router

all = ["links_router"]