"""Database session management for SQLAlchemy."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL set for the application")

# Create engine with basic configuration
engine = create_engine(
    DATABASE_URL,
    echo=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

def get_session() -> Session:
    """
    Create and return a new SQLAlchemy session.
    """
    return SessionLocal()