"""FastAPI main application entry point.

This module configures and creates the FastAPI application with all routers,
middleware, and exception handlers.
"""

# import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import (
    DomainError,
    EmailAlreadyExistsError,
    InvalidEmailError,
    InvalidNameError,
    UserNotFoundError,
)
from src.infrastructure.api.routes.user_routes import router as user_router

# Application metadata
APP_TITLE = "Tardigrade API"
APP_DESCRIPTION = """
Backend API for Tardigrade Project.

## Features

* **Users**: CRUD operations for user management
* **Authentication**: JWT-based authentication

## Architecture

This API follows hexagonal architecture (ports and adapters) with:
- Domain layer: Business logic and entities
- Application layer: Use cases and port definitions
- Infrastructure layer: External adapters (database, API)
"""
APP_VERSION = "1.0.0"

# Create FastAPI application
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)


# Exception handlers
@app.exception_handler(InvalidEmailError)
async def invalid_email_handler(request: Request, exc: InvalidEmailError) -> JSONResponse:
    """Handle invalid email errors."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(InvalidNameError)
async def invalid_name_handler(request: Request, exc: InvalidNameError) -> JSONResponse:
    """Handle invalid name errors."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request: Request, exc: UserNotFoundError) -> JSONResponse:
    """Handle user not found errors."""
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )


@app.exception_handler(EmailAlreadyExistsError)
async def email_exists_handler(request: Request, exc: EmailAlreadyExistsError) -> JSONResponse:
    """Handle email already exists errors."""
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    """Handle generic domain errors."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


# Include routers
app.include_router(user_router)


# Health check endpoint
@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Check if the API is running.",
)
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Welcome message and API information.",
)
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Tardigrade API",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": APP_VERSION,
    }
