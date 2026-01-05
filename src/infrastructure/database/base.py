"""Database base configuration.

This module provides SQLAlchemy Base class and async engine setup
for database connections following the repository pattern.
"""

import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """SQLAlchemy declarative base class.

    All database models should inherit from this class.
    """

    pass


# Module-level variables for lazy initialization
_engine: AsyncEngine | None = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_database_url() -> str:
    """Get database URL from environment.

    Returns:
        Database connection string.
    """
    return os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/tardigrade")


def get_engine() -> AsyncEngine:
    """Get or create the async database engine.

    Uses lazy initialization to avoid import-time database connections.

    Returns:
        AsyncEngine: SQLAlchemy async engine instance.
    """
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            get_database_url(),
            echo=os.getenv("DEBUG", "false").lower() == "true",
            pool_pre_ping=True,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Get or create the async session factory.

    Returns:
        async_sessionmaker: Factory for creating async sessions.
    """
    global _async_session_factory
    if _async_session_factory is None:
        _async_session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_factory


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for dependency injection.

    Yields:
        AsyncSession: Database session for executing queries.

    Example:
        @router.get("/users")
        async def get_users(session: AsyncSession = Depends(get_session)):
            ...
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
