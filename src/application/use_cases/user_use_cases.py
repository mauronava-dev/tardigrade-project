"""User use cases for the application layer.

This module contains use cases that orchestrate user-related business operations.
Use cases coordinate between domain entities and repository ports.
"""

from src.application.interfaces.repository_port import UserRepositoryPort
from src.domain.entities.user import User
from src.domain.exceptions import EmailAlreadyExistsError, UserNotFoundError


class CreateUserUseCase:
    """Use case for creating a new user.

    Validates user data and ensures email uniqueness before persisting.
    """

    def __init__(self, repository: UserRepositoryPort):
        """Initialize the use case with a repository.

        Args:
            repository: The user repository port implementation.
        """
        self.repository = repository

    async def execute(self, email: str, name: str) -> User:
        """Create a new user.

        Args:
            email: The user's email address.
            name: The user's display name.

        Returns:
            The created User entity.

        Raises:
            InvalidEmailError: If email format is invalid.
            InvalidNameError: If name is too short.
            EmailAlreadyExistsError: If email is already registered.
        """
        user = User(id=None, email=email, name=name)
        user.validate()

        existing = await self.repository.get_by_email(email)
        if existing:
            raise EmailAlreadyExistsError(email)

        return await self.repository.save(user)


class GetUserUseCase:
    """Use case for retrieving a user by ID."""

    def __init__(self, repository: UserRepositoryPort):
        """Initialize the use case with a repository.

        Args:
            repository: The user repository port implementation.
        """
        self.repository = repository

    async def execute(self, user_id: int) -> User:
        """Retrieve a user by their ID.

        Args:
            user_id: The unique identifier of the user.

        Returns:
            The User entity.

        Raises:
            UserNotFoundError: If user with given ID does not exist.
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)
        return user


class ListUsersUseCase:
    """Use case for listing users with pagination."""

    def __init__(self, repository: UserRepositoryPort):
        """Initialize the use case with a repository.

        Args:
            repository: The user repository port implementation.
        """
        self.repository = repository

    async def execute(self, skip: int = 0, limit: int = 100) -> list[User]:
        """List users with pagination.

        Args:
            skip: Number of records to skip.
            limit: Maximum number of records to return.

        Returns:
            List of User entities.
        """
        return await self.repository.list_all(skip=skip, limit=limit)


class DeleteUserUseCase:
    """Use case for deleting a user."""

    def __init__(self, repository: UserRepositoryPort):
        """Initialize the use case with a repository.

        Args:
            repository: The user repository port implementation.
        """
        self.repository = repository

    async def execute(self, user_id: int) -> bool:
        """Delete a user by their ID.

        Args:
            user_id: The unique identifier of the user to delete.

        Returns:
            True if user was deleted.

        Raises:
            UserNotFoundError: If user with given ID does not exist.
        """
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id)

        return await self.repository.delete(user_id)
