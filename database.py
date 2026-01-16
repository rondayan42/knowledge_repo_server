"""
SQLAlchemy database configuration for Knowledge Repository
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import config

# Create engine from DATABASE_URL
engine = create_engine(
    config.DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=config.DEBUG  # Log SQL in debug mode
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for ORM models
Base = declarative_base()


def get_db():
    """
    Get a database session.
    Usage:
        db = get_db()
        try:
            # use db
        finally:
            db.close()
    """
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise


def init_db():
    """Initialize database tables from ORM models."""
    from models.orm import (
        User, Category, Department, Priority, Tag,
        Article, ArticleTag, Attachment, UserFavorite, RecentlyViewed
    )
    Base.metadata.create_all(bind=engine)
    print('✅ Database tables created via SQLAlchemy')
