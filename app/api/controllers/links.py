"""
Link controller (endpoints) for URL Shortener API.
Implements all four required endpoints with TTL (bonus feature) and proper error handling.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.repositories.link_repository import LinkRepository
from app.services.link_service import LinkService
from app.api.controller_schemas.requests.link_request import LinkCreateRequest
from app.api.controller_schemas.responses.link_response import (
    LinkCreateResponse,
    LinksListResponse,
    LinkDeleteResponse,
    ErrorResponse,
    LinkData
)
from app.exceptions import (
    LinkNotFoundError,
    InvalidURLError,
    InvalidShortCodeError,
    ShortCodeAlreadyExistsError,
    ShortCodeGenerationError,
    DatabaseError,
    EmptyURLError,
    InvalidURLFormatError,
    LinkExpiredError,
    InvalidShortCodeCharactersError
)


router = APIRouter()


def get_link_service(session: Session = Depends(get_session)) -> LinkService:
    """Create LinkService with injected dependencies (Constructor Injection)."""
    repository = LinkRepository(session)
    service = LinkService(repository)
    return service

@router.post(
    "/links",
    response_model=LinkCreateResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "Short code already exists"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Create short link",
    description="Create a new shortened URL from an original URL. TTL is automatically applied if configured.",
    tags=["links"]
)
def create_short_link(
        request: LinkCreateRequest,
        service: LinkService = Depends(get_link_service)
):
    """Create a new short link."""
    try:

        link_dict = service.create_short_link(str(request.original_url))

        link_data = LinkData(**link_dict)

        return LinkCreateResponse(status="success", data=link_data)

    except (EmptyURLError, InvalidURLError, InvalidURLFormatError,
            InvalidShortCodeError, InvalidShortCodeCharactersError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except ShortCodeAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except (ShortCodeGenerationError, DatabaseError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "failure",
                "message": "Internal server error",
                "error_code": "INTERNAL_ERROR"
            }
        )


@router.get(
    "/u/{short_code}",
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        307: {"description": "Redirect to original URL"},
        400: {"model": ErrorResponse, "description": "Invalid short code format"},
        404: {"model": ErrorResponse, "description": "Link not found"},
        410: {"model": ErrorResponse, "description": "Link has expired (TTL)"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Redirect to original URL",
    description="Use short code to redirect to original URL. Checks TTL expiration.",
    tags=["links"]
)
def redirect_to_original(
        short_code: str,
        service: LinkService = Depends(get_link_service)
):
    """Redirect to original URL using short code."""
    try:

        original_url = service.get_original_url(short_code)

        return RedirectResponse(
            url=original_url,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )

    except LinkNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except LinkExpiredError as e:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except (InvalidShortCodeError, InvalidShortCodeCharactersError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "failure",
                "message": e.detail,
                "error_code": e.error_code
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": "failure",
                "message": "Internal server error",
                "error_code": "INTERNAL_ERROR"
            }
        )

