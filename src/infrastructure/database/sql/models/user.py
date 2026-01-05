"""SQLAlchemy User model.

This module defines the database model for users, mapping the domain
User entity to the database schema.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.infrastructure.database.base import Base


class UserModel(Base):
    """SQLAlchemy model for users table.

    Maps to the 'users' table in the database and provides
    conversion methods to/from domain User entity.

    Attributes:
        id: Primary key, auto-incremented.
        email: Unique email address, indexed for fast lookups.
        name: User's display name.
        is_active: Whether the user account is active.
        created_at: Timestamp when the record was created.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        """Return string representation of UserModel."""
        return f"<UserModel(id={self.id}, email='{self.email}', name='{self.name}')>"
