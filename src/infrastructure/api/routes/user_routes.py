"""User API routes.

This module contains FastAPI routes for user CRUD operations.
"""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.user_use_cases import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetUserUseCase,
    ListUsersUseCase,
)
from src.infrastructure.api.schemas.user_schemas import UserCreate, UserResponse, UserUpdate
from src.infrastructure.database.base import get_session
from src.infrastructure.database.sql.repositories.user_repository import SQLUserRepository

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a new user account. Email must be unique.",
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "Invalid input data"},
        409: {"description": "Email already exists"},
    },
)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Create a new user.

    - **email**: unique email address
    - **name**: user display name (2-100 characters)
    """
    repository = SQLUserRepository(session)
    use_case = CreateUserUseCase(repository)
    user = await use_case.execute(user_data.email, user_data.name)
    return UserResponse.from_entity(user)


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="List all users",
    description="Retrieve a paginated list of all users.",
    responses={
        200: {"description": "List of users"},
    },
)
async def list_users(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    session: AsyncSession = Depends(get_session),
) -> list[UserResponse]:
    """List users with pagination."""
    repository = SQLUserRepository(session)
    use_case = ListUsersUseCase(repository)
    users = await use_case.execute(skip=skip, limit=limit)
    return [UserResponse.from_entity(user) for user in users]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique identifier.",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
    },
)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Get a user by their ID."""
    repository = SQLUserRepository(session)
    use_case = GetUserUseCase(repository)
    user = await use_case.execute(user_id)
    return UserResponse.from_entity(user)


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user's information.",
    responses={
        200: {"description": "User updated successfully"},
        400: {"description": "Invalid input data"},
        404: {"description": "User not found"},
    },
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Update a user's information."""
    repository = SQLUserRepository(session)

    # Get existing user
    get_use_case = GetUserUseCase(repository)
    user = await get_use_case.execute(user_id)

    # Update fields if provided
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    # Validate and save
    user.validate()
    updated_user = await repository.save(user)
    return UserResponse.from_entity(updated_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user by their unique identifier.",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found"},
    },
)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a user by their ID."""
    repository = SQLUserRepository(session)
    use_case = DeleteUserUseCase(repository)
    await use_case.execute(user_id)
