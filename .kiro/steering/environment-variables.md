# Environment Variables

## Reading Environment Variables

Always use `os.getenv()` with a default value:

```python
import os

# Correct usage
database_url = os.getenv("DATABASE_URL", "postgresql://localhost:5432/dev")
debug_mode = os.getenv("DEBUG", "false").lower() == "true"
api_port = int(os.getenv("API_PORT", "8000"))

# Never use os.environ directly without handling KeyError
# Avoid: os.environ["DATABASE_URL"]
```

## Common Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `postgresql://localhost:5432/dev` |
| `API_PORT` | API server port | `8000` |
| `DEBUG` | Enable debug mode | `false` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `ENVIRONMENT` | Environment name (local/qa/production) | `local` |
| `AWS_REGION` | AWS region | `us-east-1` |

## Configuration Pattern

```python
import os


class Settings:
    """Application settings loaded from environment variables."""

    database_url: str = os.getenv("DATABASE_URL", "postgresql://localhost:5432/dev")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
```
