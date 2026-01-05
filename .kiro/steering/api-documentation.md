# API Documentation Guidelines

## OpenAPI/Swagger

FastAPI generates documentation automatically. Access at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

## Documentation Requirements

All endpoints shared with clients must include:
- Summary and description
- Request/response examples
- Error responses
- Tags for grouping

## Endpoint Documentation Pattern

```python
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/v1/users", tags=["Users"])


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: str = Field(..., example="user@example.com", description="User email address")
    name: str = Field(..., example="John Doe", min_length=2, max_length=100)


class UserResponse(BaseModel):
    """Schema for user response."""

    id: int = Field(..., example=1)
    email: str = Field(..., example="user@example.com")
    name: str = Field(..., example="John Doe")


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
async def create_user(user: UserCreate) -> UserResponse:
    """
    Create a new user with the following information:

    - **email**: unique email address
    - **name**: user display name
    """
    pass
```

## API Metadata

```python
from fastapi import FastAPI

app = FastAPI(
    title="Tardigrade API",
    description="Backend API for Tardigrade Project",
    version="1.0.0",
    contact={"name": "API Support", "email": "support@example.com"},
    license_info={"name": "MIT"},
)
```
