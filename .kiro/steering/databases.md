# Database Guidelines

## Supported Databases

| Database | Type | Use Case | Library |
|----------|------|----------|---------|
| Aurora PostgreSQL | SQL | Primary transactional DB | SQLAlchemy + Alembic |
| Aurora MySQL | SQL | Transactional DB | SQLAlchemy + Alembic |
| DynamoDB | NoSQL | Key-value, high throughput | boto3 / aioboto3 |
| Redshift | Data Warehouse | Analytics, reporting | sqlalchemy-redshift |
| Redis | Cache/NoSQL | Caching, sessions, queues | redis-py / aioredis |
| MongoDB | NoSQL | Document store | motor (async) / pymongo |

## Connection Strings

```python
import os

# Aurora PostgreSQL
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@host:5432/db")

# Aurora MySQL
MYSQL_URL = os.getenv("MYSQL_URL", "mysql+aiomysql://user:pass@host:3306/db")

# Redshift
REDSHIFT_URL = os.getenv("REDSHIFT_URL", "redshift+redshift_connector://user:pass@host:5439/db")

# MongoDB
MONGO_URL = os.getenv("MONGO_URL", "mongodb://user:pass@host:27017/db")

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://host:6379/0")

# DynamoDB uses AWS credentials, not connection string
```

## Repository Pattern

Each database type implements a repository interface:

```python
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Repository(ABC, Generic[T]):
    """Base repository interface."""

    @abstractmethod
    async def get_by_id(self, id: str) -> T | None:
        pass

    @abstractmethod
    async def save(self, entity: T) -> T:
        pass
```
