"""
Response schemas for URL Shortener API.
Defines structured HTTP responses used across the application.
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class LinkData(BaseModel):
    """Data transfer object for link information.

    Used to standardize the structure of link data returned by API responses.
    """

    id: int
    original_url: str
    short_code: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    short_url: str

    class Config:
        from_attributes = True


class LinkCreateResponse(BaseModel):
    """Response for POST /links - Link created successfully."""

    status: str = "success"
    data: LinkData

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "data": {
                    "id": 1,
                    "original_url": "https://example.com",
                    "short_code": "abc123",
                    "created_at": "2024-01-10T10:30:00",
                    "expires_at": None,
                    "short_url": "/u/abc123"
                }
            }
        }


class RedirectResponse(BaseModel):
    """Schema for redirect response documentation (302 Redirect)."""

    detail: str = "Redirect to original URL"

    class Config:
        schema_extra = {
            "example": {
                "detail": "Redirect to https://example.com"
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response model.

    Every error response contains a `status` field as required by the project.
    """

    status: str = "failure"
    message: str
    error_code: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "failure",
                "message": "Link with short code 'abc123' not found",
                "error_code": "LINK_NOT_FOUND",
            }
        }


class ValidationErrorResponse(ErrorResponse):
    """Response model for validation errors (400 Bad Request)."""

    class Config:
        schema_extra = {
            "example": {
                "status": "failure",
                "message": "Invalid URL: must start with http:// or https://",
                "error_code": "INVALID_URL",
            }
        }


class NotFoundErrorResponse(ErrorResponse):
    """Response model for 404 Not Found errors."""

    class Config:
        schema_extra = {
            "example": {
                "status": "failure",
                "message": "Link not found",
                "error_code": "NOT_FOUND",
            }
        }