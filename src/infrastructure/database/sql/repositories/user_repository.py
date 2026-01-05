"""SQL User repository implementation.

This module implements the UserRepositoryPort interface using SQLAlchemy
for PostgreSQL/MySQL database operations.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.repository_port import UserRepositoryPort
from src.domain.entities.user import User
from src.infrastructure.database.sql.models.user import UserModel


class SQLUserRepository(UserRepositoryPort):
    """SQL implementation of UserRepositoryPort.

    Provides CRUD operations for User entities using SQLAlchemy
    with async support for Aurora PostgreSQL/MySQL.

    Attributes:
        session: Async database session for executing queries.
    """

    def __init__(self, session: AsyncSession) -> None:
        """Initialize repository with database session.

        Args:
            session: Async SQLAlchemy session.
        """
        self.session = session

    def _to_entity(self, model: UserModel) -> User:
        """Convert SQLAlchemy model to domain entity.

        Args:
            model: SQLAlchemy UserModel instance.

        Returns:
            Domain User entity.
        """
        return User(
            id=model.id,
            email=model.email,
            name=model.name,
            is_active=model.is_active,
            created_at=model.created_at,
        )

    def _to_model(self, entity: User) -> UserModel:
        """Convert domain entity to SQLAlchemy model.

        Args:
            entity: Domain User entity.

        Returns:
            SQLAlchemy UserModel instance.
        """
        model = UserModel(
            email=entity.email,
            name=entity.name,
            is_active=entity.is_active,
        )
        if entity.id is not None:
            model.id = entity.id
        if entity.created_at is not None:
            model.created_at = entity.created_at
        return model

    async def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The User entity if found, None otherwise.
        """
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The User entity if found, None otherwise.
        """
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def save(self, user: User) -> User:
        """Persist a user entity.

        Creates a new user if id is None, otherwise updates existing user.

        Args:
            user: The User entity to persist.

        Returns:
            The persisted User entity with updated id and timestamps.
        """
        if user.id is None:
            # Create new user
            model = self._to_model(user)
            self.session.add(model)
            await self.session.flush()
            await self.session.refresh(model)
            return self._to_entity(model)
        else:
            # Update existing user
            result = await self.session.execute(select(UserModel).where(UserModel.id == user.id))
            model = result.scalar_one_or_none()
            if model:
                model.email = user.email
                model.name = user.name
                model.is_active = user.is_active
                await self.session.flush()
                await self.session.refresh(model)
                return self._to_entity(model)
            else:
                # User not found, create new
                model = self._to_model(user)
                self.session.add(model)
                await self.session.flush()
                await self.session.refresh(model)
                return self._to_entity(model)

    async def delete(self, user_id: int) -> bool:
        """Delete a user by their unique identifier.

        Args:
            user_id: The unique identifier of the user to delete.

        Returns:
            True if the user was deleted, False if user was not found.
        """
        result = await self.session.execute(select(UserModel).where(UserModel.id == user_id))
        model = result.scalar_one_or_none()
        if model:
            await self.session.delete(model)
            await self.session.flush()
            return True
        return False

    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Retrieve a paginated list of all users.

        Args:
            skip: Number of records to skip (for pagination).
            limit: Maximum number of records to return.

        Returns:
            List of User entities.
        """
        result = await self.session.execute(select(UserModel).offset(skip).limit(limit))
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]
