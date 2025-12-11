from fastapi import HTTPException, status
from typing import Any, Optional, Dict


class URLShortenerError(HTTPException):
    """Base exception for all URL Shortener errors"""

    def __init__(
            self,
            status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail: str = "An error occurred",
            headers: Optional[Dict[str, str]] = None,
            error_code: Optional[str] = None
    ):
        self.error_code = error_code or self.__class__.__name__
        super().__init__(
            status_code=status_code,
            detail=detail,
            headers=headers
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API response"""
        return {
            "status": "failure",
            "message": self.detail,
            "error_code": self.error_code
        }


class ValidationError(URLShortenerError):
    """Base exception for validation errors"""

    def __init__(
            self,
            detail: str = "Validation error",
            error_code: str = "VALIDATION_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class NotFoundError(URLShortenerError):
    """Base exception for not found errors"""

    def __init__(
            self,
            detail: str = "Resource not found",
            error_code: str = "NOT_FOUND_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code=error_code
        )


class ConflictError(URLShortenerError):
    """Base exception for conflict errors"""

    def __init__(
            self,
            detail: str = "Conflict occurred",
            error_code: str = "CONFLICT_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code
        )


class ServerError(URLShortenerError):
    """Base exception for server errors"""

    def __init__(
            self,
            detail: str = "Internal server error",
            error_code: str = "SERVER_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )


class BadRequestError(URLShortenerError):
    """Base exception for bad request errors"""

    def __init__(
            self,
            detail: str = "Bad request",
            error_code: str = "BAD_REQUEST_ERROR"
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )