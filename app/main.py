"""
URL Shortener API - FastAPI application entry point.

Run with:
    uvicorn main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import router as api_router


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title="URL Shortener API",
        description=(
            "A RESTful API for shortening URLs with TTL support. "
            "Midterm project for Software Engineering Course."
        ),
        version="1.0.0",
        docs_url="/docs"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    return app


# Create the FastAPI application instance
app = create_application()


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint providing API information.

    Returns:
        dict: API metadata and available endpoints
    """
    return {
        "application": "URL Shortener API",
        "version": "1.0.0",
        "description": "RESTful API for shortening URLs with TTL support",
        "endpoints": {
            "create_link": "POST /api/v1/links",
            "redirect": "GET /api/v1/u/{short_code}",
            "list_links": "GET /api/v1/links",
            "delete_link": "DELETE /api/v1/links/{short_code}",
        },
        "documentation": {
            "swagger_ui": "/docs"
        },
        "note": "URL Shortener Midterm Project - Software Engineering Course"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "service": "url-shortener",
        "version": "1.0.0"
    }


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Run the FastAPI development server.

    Args:
        host: Server host address
        port: Server port
        reload: Enable auto-reload on code changes
    """
    import uvicorn

    print("🚀 Starting URL Shortener API Server...")
    print(f"   URL: http://{host}:{port}")
    print(f"   Docs: http://{host}:{port}/docs")
    print("\n📋 Available Endpoints:")
    print("   • POST /api/v1/links              - Create short link")
    print("   • GET  /api/v1/u/{short_code}     - Redirect to original URL")
    print("   • GET  /api/v1/links              - List all links")
    print("   • DELETE /api/v1/links/{short_code} - Delete a link")
    print("\n⚡ Press Ctrl+C to stop the server")

    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    run_server()