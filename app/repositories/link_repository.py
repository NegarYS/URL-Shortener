from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.link import Link
from app.exceptions import (
    LinkNotFoundError,
    ShortCodeAlreadyExistsError,
    DatabaseError
)


class LinkRepository:
    """Repository layer for Link model operations.

    Implements data access layer with proper error handling.
    Follows constructor injection principle.
    """

    def __init__(self, session: Session):
        """Initialize repository with a database session.

        Args:
            session: SQLAlchemy database session (injected)
        """
        self.session = session

    def create(self, original_url: str, short_code: str) -> Link:
        """Create a new shortened link.

        Args:
            original_url: The original long URL
            short_code: The generated short code (6 chars)

        Returns:
            Link: The created link object

        Raises:
            ShortCodeAlreadyExistsError: If short_code already exists
            DatabaseError: For other database errors
        """
        try:

            link = Link(original_url=original_url, short_code=short_code)

            self.session.add(link)
            self.session.commit()
            self.session.refresh(link)

            return link

        except IntegrityError as e:
            self.session.rollback()

            if "short_code" in str(e).lower() and "unique" in str(e).lower():
                raise ShortCodeAlreadyExistsError(short_code)

            raise DatabaseError("create link", str(e))

        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseError("create link", str(e))

    def get_by_id(self, link_id: int) -> Optional[Link]:
        """Get link by its ID.

        Args:
            link_id: The link ID

        Returns:
            Optional[Link]: Link if found, None otherwise

        Raises:
            DatabaseError: For database errors
        """
        try:
            return self.session.get(Link, link_id)
        except SQLAlchemyError as e:
            raise DatabaseError(f"get link by id {link_id}", str(e))

    def get_by_short_code(self, short_code: str) -> Link:
        """Get link by short code.

        Args:
            short_code: The short code (6 chars)

        Returns:
            Link: The link object

        Raises:
            LinkNotFoundError: If link not found
            DatabaseError: For database errors
        """
        try:
            # Use SQLAlchemy 2.0 select syntax
            stmt = select(Link).where(Link.short_code == short_code)
            result = self.session.execute(stmt)
            link = result.scalar_one_or_none()

            if not link:
                raise LinkNotFoundError(short_code)

            return link

        except SQLAlchemyError as e:
            raise DatabaseError(f"get link by short code {short_code}", str(e))

    def get_by_original_url(self, original_url: str) -> Optional[Link]:
        """Get link by original URL (for duplicate checking).

        Args:
            original_url: The original URL to search for

        Returns:
            Optional[Link]: Link if found, None otherwise

        Raises:
            DatabaseError: For database errors
        """
        try:
            stmt = select(Link).where(Link.original_url == original_url)
            result = self.session.execute(stmt)
            return result.scalar_one_or_none()

        except SQLAlchemyError as e:
            raise DatabaseError(f"get link by original URL", str(e))

    def exists(self, short_code: str) -> bool:
        """Check if a short code already exists.

        Args:
            short_code: The short code to check

        Returns:
            bool: True if exists, False otherwise

        Raises:
            DatabaseError: For database errors
        """
        try:
            stmt = select(Link.id).where(Link.short_code == short_code).limit(1)
            result = self.session.execute(stmt)
            return result.scalar_one_or_none() is not None

        except SQLAlchemyError as e:
            raise DatabaseError(f"check existence of {short_code}", str(e))

