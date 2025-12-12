"""
Service layer for URL Shortener.
Contains business logic for link operations.
Follows constructor injection principle.
"""

import random
import re
from datetime import datetime, timedelta
from typing import Optional

from app.repositories.link_repository import LinkRepository
from app.exceptions import (
    EmptyURLError,
    InvalidURLError,
    InvalidURLFormatError,
    ShortCodeGenerationError,
    InvalidShortCodeError,
    InvalidShortCodeCharactersError,
    LinkExpiredError,
    LinkNotFoundError,
    DatabaseError
)
from app.config import config


class LinkService:
    """Service layer for link operations."""

    def __init__(self, repository: LinkRepository):
        """Initialize service with repository dependency.

        Args:
            repository: LinkRepository instance (injected)
        """
        self.repository = repository

    def validate_url(self, url: str) -> bool:
        """Validate URL format and content.

        Args:
            url: The URL to validate

        Returns:
            bool: True if URL is valid

        Raises:
            EmptyURLError: If URL is empty
            InvalidURLError: If URL doesn't start with http/https
            InvalidURLFormatError: If URL has invalid format
        """

        if not url or url.strip() == "":
            raise EmptyURLError()

        if not url.startswith(('http://', 'https://')):
            raise InvalidURLError(url)

        url_pattern = re.compile(
            r'^https?://'  
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  
            r'localhost|'  
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
            r'(?::\d+)?'  
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not url_pattern.match(url):
            raise InvalidURLFormatError(url)

        return True

    def _generate_short_code(self) -> str:
        """Generate a random short code.

        Returns:
            str: Random short code (6 characters)

        Note:
            Uses method 1 from PDF (Random Generation)
        """
        alphabet = config.short_code_alphabet
        length = config.SHORT_CODE_LENGTH

        return ''.join(random.choices(alphabet, k=length))

    def _validate_short_code_format(self, short_code: str) -> bool:
        """Validate short code format.

        Args:
            short_code: The short code to validate

        Returns:
            bool: True if format is valid

        Raises:
            InvalidShortCodeError: If length is not 6
            InvalidShortCodeCharactersError: If contains invalid chars
        """
        # Check length
        if len(short_code) != config.SHORT_CODE_LENGTH:
            raise InvalidShortCodeError(short_code)

        # Check characters (must be Base62: a-zA-Z0-9)
        alphabet = config.short_code_alphabet
        for char in short_code:
            if char not in alphabet:
                raise InvalidShortCodeCharactersError(short_code)

        return True

    def generate_unique_short_code(self) -> str:
        """Generate a unique short code that doesn't exist in database.

        Returns:
            str: Unique short code

        Raises:
            ShortCodeGenerationError: If unable to generate unique code
        """
        max_attempts = config.SHORT_CODE_MAX_ATTEMPTS

        for attempt in range(max_attempts):
            short_code = self._generate_short_code()

            if not self.repository.exists(short_code):
                return short_code

        raise ShortCodeGenerationError(max_attempts)

    def _calculate_expires_at(self) -> Optional[datetime]:
        """Calculate expiration time if TTL is enabled.

        Returns:
            Optional[datetime]: Expiration time or None if TTL disabled
        """
        if config.APP_TTL_HOURS > 0:
            return datetime.now() + timedelta(hours=config.APP_TTL_HOURS)
        return None

    def create_short_link(self, original_url: str) -> dict:
        """Create a new short link.

        Args:
            original_url: The original URL to shorten

        Returns:
            dict: Dictionary containing link information

        Raises:
            Validation errors: If URL is invalid
            ShortCodeGenerationError: If unable to generate unique code
        """
        # 1. Validate URL
        self.validate_url(original_url)

        short_code = self.generate_unique_short_code()

        expires_at = self._calculate_expires_at()

        link = self.repository.create(
            original_url=original_url,
            short_code=short_code,
            expires_at=expires_at
        )

        short_url = f"/u/{short_code}"

        return {
            "id": link.id,
            "original_url": link.original_url,
            "short_code": link.short_code,
            "short_url": short_url,
            "created_at": link.created_at,
            "expires_at": expires_at
        }

    def get_original_url(self, short_code: str) -> str:
        """Get original URL from short code.

        Args:
            short_code: The short code

        Returns:
            str: Original URL

        Raises:
            InvalidShortCodeError: If short code format is invalid
        """

        self._validate_short_code_format(short_code)

        if self.repository.is_expired(short_code):
            raise LinkExpiredError(short_code)

        link = self.repository.get_by_short_code(short_code)

        return link.original_url

    def get_all_links(self, skip: int = 0, limit: int = 100, include_expired: bool = False) -> list:
        """Get all shortened links.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            list: List of link dictionaries
        """
        links = self.repository.get_all(skip=skip, limit=limit, include_expired=include_expired)

        result = []
        for link in links:
            result.append({
                "id": link.id,
                "original_url": link.original_url,
                "short_code": link.short_code,
                "short_url": f"/u/{link.short_code}",
                "created_at": link.created_at,
                "expires_at": link.expires_at
            })

        return result

    def delete_link(self, short_code: str) -> bool:
        """Delete a short link.

        Args:
            short_code: The short code to delete

        Returns:
            bool: True if deleted successfully

        Raises:
            InvalidShortCodeError: If short code format is invalid
        """
        self._validate_short_code_format(short_code)

        return self.repository.delete(short_code)


    def delete_expired_links(self) -> int:
        """Delete expired links (TTL bonus feature).

        Returns:
            int: Number of deleted links
        """
        if config.APP_TTL_HOURS <= 0:
            return 0  # TTL not enabled

        return self.repository.delete_expired_links()

    def is_expired(self, short_code: str) -> bool:
        """Check if a link is expired (TTL feature).

        Args:
            short_code: The short code to check

        Returns:
            bool: True if expired, False otherwise

        Raises:
            InvalidShortCodeError: If short code format is invalid
            LinkNotFoundError: If link not found
        """

        self._validate_short_code_format(short_code)

        return self.repository.is_expired(short_code)

    def count_links(self) -> dict:
        """Get statistics about links including TTL information.

        Returns:
            dict: Statistics about links
        """
        total = self.repository.count()

        return {
            "total": total,
            "ttl_hours": config.APP_TTL_HOURS,
            "short_code_length": config.SHORT_CODE_LENGTH
        }