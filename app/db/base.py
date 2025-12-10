from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class Base(DeclarativeBase, MappedAsDataclass):
    """Base class for SQLAlchemy models."""
    pass