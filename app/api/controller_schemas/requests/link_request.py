"""
Request schemas for URL Shortener API.
"""

from pydantic import BaseModel, HttpUrl, Field
from typing import List


class LinkCreateRequest(BaseModel):
    """Request schema for POST /links - Create short link."""

    original_url: HttpUrl = Field(
        ...,
        description="The original URL to shorten",
        examples=["https://aut.ac.ir", "https://example.com"]
    )

    class Config:
        schema_extra = {
            "example": {
                "original_url": "https://example.com"
            }
        }
