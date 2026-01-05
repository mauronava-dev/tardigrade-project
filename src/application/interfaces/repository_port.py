"""Repository port interface for user persistence.

This module defines the abstract interface (port) for user repository operations.
Infrastructure adapters implement this interface to provide concrete persistence.
"""

from abc import ABC, abstractmethod

from src.domain.entities.user import User


class UserRepositoryPort(ABC):
    """Abstract interface for user repository operations.

    This port defines the contract that any user repository adapter must implement.
    Following hexagonal architecture, this keeps the application layer independent
    of specific database implementations.
    """

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """Retrieve a user by their unique identifier.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The User entity if found, None otherwise.
        """
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """Retrieve a user by their email address.

        Args:
            email: The email address to search for.

        Returns:
            The User entity if found, None otherwise.
        """
        pass

    @abstractmethod
    async def save(self, user: User) -> User:
        """Persist a user entity.

        Creates a new user if id is None, otherwise updates existing user.

        Args:
            user: The User entity to persist.

        Returns:
            The persisted User entity with updated id and timestamps.
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """Delete a user by their unique identifier.

        Args:
            user_id: The unique identifier of the user to delete.

        Returns:
            True if the user was deleted, False if user was not found.
        """
        pass

    @abstractmethod
    async def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        """Retrieve a paginated list of all users.

        Args:
            skip: Number of records to skip (for pagination).
            limit: Maximum number of records to return.

        Returns:
            List of User entities.
        """
        pass
