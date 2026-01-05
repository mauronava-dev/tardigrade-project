"""User Pydantic schemas for API request/response validation.

This module contains Pydantic models for user-related API operations.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from src.domain.entities.user import User


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: str = Field(..., example="user@example.com", description="User email address")
    name: str = Field(..., min_length=2, max_length=100, example="John Doe", description="User display name")


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""

    email: str | None = Field(None, example="user@example.com", description="User email address")
    name: str | None = Field(None, min_length=2, max_length=100, example="John Doe", description="User display name")
    is_active: bool | None = Field(None, description="Whether the user account is active")


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int = Field(..., example=1, description="Unique user identifier")
    email: str = Field(..., example="user@example.com", description="User email address")
    name: str = Field(..., example="John Doe", description="User display name")
    is_active: bool = Field(..., example=True, description="Whether the user account is active")
    created_at: datetime = Field(..., description="Timestamp when the user was created")

    model_config = {"from_attributes": True}

    @classmethod
    def from_entity(cls, user: User) -> "UserResponse":
        """Create a UserResponse from a User domain entity.

        Args:
            user: The User domain entity.

        Returns:
            UserResponse instance.
        """
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            is_active=user.is_active,
            created_at=user.created_at,
        )
