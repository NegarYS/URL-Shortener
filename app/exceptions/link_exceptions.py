from .base import (
    URLShortenerError,
    ValidationError,
    NotFoundError,
    ConflictError,
    ServerError,
    BadRequestError
)


class LinkNotFoundError(NotFoundError):
    """Raised when a link with a given short code does not exist."""

    def __init__(self, short_code: str):
        detail = f"Link with short code '{short_code}' not found"
        super().__init__(
            detail=detail,
            error_code="LINK_NOT_FOUND"
        )


class ShortCodeAlreadyExistsError(ConflictError):
    """Raised when trying to create a link with a short code that already exists."""

    def __init__(self, short_code: str):
        detail = f"Short code '{short_code}' already exists"
        super().__init__(
            detail=detail,
            error_code="SHORT_CODE_EXISTS"
        )


class InvalidURLError(ValidationError):
    """Raised when the provided URL is invalid."""

    def __init__(self, url: str = None):
        if url:
            detail = f"Invalid URL: '{url}'. URL must start with http:// or https://"
        else:
            detail = "Invalid URL. URL must start with http:// or https://"
        super().__init__(
            detail=detail,
            error_code="INVALID_URL"
        )


class EmptyURLError(ValidationError):
    """Raised when URL is empty ."""

    def __init__(self):
        detail = "URL cannot be empty"
        super().__init__(
            detail=detail,
            error_code="EMPTY_URL"
        )


class URLTooLongError(ValidationError):
    """Raised when URL is too long."""

    def __init__(self, max_length: int = 2048):
        detail = f"URL is too long. Maximum length is {max_length} characters"
        super().__init__(
            detail=detail,
            error_code="URL_TOO_LONG"
        )


class InvalidURLFormatError(ValidationError):
    """Raised when URL has invalid format."""

    def __init__(self, url: str):
        detail = f"Invalid URL format: '{url}'. Please provide a valid URL"
        super().__init__(
            detail=detail,
            error_code="INVALID_URL_FORMAT"
        )


class ShortCodeGenerationError(ServerError):
    """Raised when unable to generate a unique short code."""

    def __init__(self, max_attempts: int = 10):
        detail = f"Failed to generate unique short code after {max_attempts} attempts"
        super().__init__(
            detail=detail,
            error_code="SHORT_CODE_GENERATION_FAILED"
        )


class LinkExpiredError(URLShortenerError):
    """Raised when a link has expired (for TTL feature)."""

    def __init__(self, short_code: str):
        detail = f"Link '{short_code}' has expired"
        super().__init__(
            status_code=410,  # 410 Gone
            detail=detail,
            error_code="LINK_EXPIRED"
        )


class DatabaseError(ServerError):
    """Raised for database-related errors."""

    def __init__(self, operation: str, error: str):
        detail = f"Database error during {operation}: {error}"
        super().__init__(
            detail=detail,
            error_code="DATABASE_ERROR"
        )


class OriginalURLNotFoundError(NotFoundError):
    """Raised when original URL is not found in database."""

    def __init__(self, url: str = None):
        if url:
            detail = f"Original URL '{url}' not found"
        else:
            detail = "Original URL not found"
        super().__init__(
            detail=detail,
            error_code="ORIGINAL_URL_NOT_FOUND"
        )


class InvalidShortCodeError(ValidationError):
    """Raised when short code format is invalid."""

    def __init__(self, short_code: str):
        detail = f"Invalid short code format: '{short_code}'. Must be 6 alphanumeric characters"
        super().__init__(
            detail=detail,
            error_code="INVALID_SHORT_CODE"
        )


class InvalidShortCodeCharactersError(ValidationError):
    """Raised when short code contains invalid characters."""

    def __init__(self, short_code: str):
        detail = f"Short code '{short_code}' contains invalid characters. Only a-z A-Z 0-9 allowed"
        super().__init__(
            detail=detail,
            error_code="INVALID_SHORT_CODE_CHARACTERS"
        )





