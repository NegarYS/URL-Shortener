from datetime import datetime
from typing import Optional

from sqlalchemy import Text, String, DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Link(Base):
    """
    Represents a shortened link stored in the database.

    Attributes:
        id (int): Auto-incremented primary key of the link.
        original_url (str): The original (long) URL.
        short_code (str): The generated short code for the URL.
        created_at (datetime): Timestamp indicating when the link was created.
    """

    __tablename__ = "links"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        init=False,
    )

    original_url: Mapped[str] = mapped_column(Text)

    short_code: Mapped[str] = mapped_column(
        String(6),
        unique=True,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        init=False,
    )

    def __repr__(self) -> str:
        """Return a string representation of the Link object."""
        return f"Link(id={self.id}, short_code={self.short_code})"
