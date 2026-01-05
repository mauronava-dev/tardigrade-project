# Logging Guidelines

## Stack

- `structlog` for structured logging
- JSON format for production (CloudWatch compatible)
- Console format for local development

## Configuration

```python
import os
import structlog


def configure_logging() -> None:
    """Configure structlog based on environment."""
    environment = os.getenv("ENVIRONMENT", "local")

    if environment == "production":
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ]
    else:
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(colors=True)
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
```

## Usage Pattern

```python
import structlog

logger = structlog.get_logger(__name__)

# Basic logging
logger.info("user_created", user_id=123)
logger.error("payment_failed", order_id=456, reason="insufficient_funds")

# With request context (middleware)
logger.info("request_received", method="POST", path="/api/users", request_id="abc-123")
```
