"""
Application configuration loaded from environment variables.

This module provides centralized configuration management following
the twelve-factor app methodology.
"""

import os


class Settings:
    """
    Application settings loaded from environment variables.

    All settings have sensible defaults for local development.
    Production environments should set appropriate values via
    environment variables or secrets management.
    """

    # Database Configuration
    database_url: str = os.getenv(
        "DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/tardigrade"
    )

    # API Configuration
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_host: str = os.getenv("API_HOST", "0.0.0.0")

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "local")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # JWT Authentication
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # AWS Configuration
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

    # Redis Configuration
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # MongoDB Configuration
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017/tardigrade")

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    @property
    def is_local(self) -> bool:
        """Check if running in local development environment."""
        return self.environment == "local"


# Singleton instance for application-wide use
settings = Settings()
