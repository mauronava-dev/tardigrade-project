# Hexagonal Architecture Guidelines

## Overview

This project follows hexagonal architecture (ports and adapters) to maintain clean separation of concerns.

## Directory Structure

```
src/
├── domain/           # Business logic and entities
│   ├── entities/     # Domain models
│   ├── services/     # Domain services
│   ├── prompts/      # Prompt templates (value objects)
│   └── exceptions/   # Domain-specific exceptions
├── application/      # Use cases and application services
│   ├── use_cases/    # Application use cases
│   └── interfaces/   # Port definitions (abstract classes)
│       └── llm_port.py  # LLM abstraction for AI agents
├── infrastructure/   # External adapters
│   ├── database/     # Database adapters
│   │   ├── sql/      # SQLAlchemy models (Aurora PostgreSQL/MySQL)
│   │   ├── dynamodb/ # DynamoDB repositories
│   │   ├── mongo/    # MongoDB repositories
│   │   └── redis/    # Redis cache adapter
│   ├── api/          # FastAPI routes and schemas
│   └── external/     # Third-party service integrations
│       └── bedrock/  # Amazon Bedrock adapter
└── shared/           # Shared utilities and constants
```

## Key Principles

1. Domain layer has no external dependencies
2. Application layer orchestrates domain logic
3. Infrastructure adapts external systems to domain interfaces
4. Dependencies point inward (infrastructure -> application -> domain)
