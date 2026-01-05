<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform"/>
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS"/>
</p>

# 🦠 Tardigrade Project

> *Like the tardigrade, your code will survive anything.*

A production-ready Python backend template designed for AI-powered IDEs. Built with hexagonal architecture, comprehensive tooling, and infrastructure-as-code from day one.

---

## ✨ Why Tardigrade?

- **🤖 AI-First Development** — Optimized for Kiro, Cursor, and GitHub Copilot with steering files and structured prompts
- **🏗️ Hexagonal Architecture** — Clean separation of concerns with ports and adapters pattern
- **🚀 Production Ready** — Docker, Terraform, and CI/CD pipelines included out of the box
- **📊 Multi-Database Support** — PostgreSQL, MySQL, DynamoDB, Redis, MongoDB, and Redshift
- **🔐 Security Built-in** — JWT authentication, environment-based secrets, and OIDC deployments
- **🧪 Quality Enforced** — 80% coverage minimum, pre-commit hooks, and automated linting

---

## 📁 Project Structure

```
tardigrade/
├── src/
│   ├── domain/              # Business logic (no external dependencies)
│   │   ├── entities/        # Domain models
│   │   ├── services/        # Domain services
│   │   ├── prompts/         # AI prompt templates
│   │   └── exceptions/      # Domain exceptions
│   ├── application/         # Use cases and ports
│   │   ├── use_cases/       # Application logic
│   │   └── interfaces/      # Port definitions (LLM, repositories)
│   ├── infrastructure/      # External adapters
│   │   ├── database/        # SQL, DynamoDB, Redis, MongoDB
│   │   ├── api/             # FastAPI routes and schemas
│   │   └── external/        # Third-party integrations (Bedrock)
│   └── shared/              # Utilities and constants
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── factories/           # Test data factories
├── scripts/                 # Development scripts
├── docker/                  # Docker configurations
│   ├── local/
│   ├── qa/
│   └── production/
├── terraform/               # Infrastructure as code
│   ├── local/
│   ├── qa/
│   └── production/
└── docs/
    └── user/                # Developer documentation (gitignored)
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Terraform (for infrastructure)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/tardigrade.git
cd tardigrade

# Run setup script (creates venv, installs deps, configures git hooks)
./scripts/setup.sh

# Start development environment
./scripts/run.sh
```

### Using Docker

```bash
# Start all services (API + PostgreSQL + Redis)
docker compose -f docker/local/docker-compose.yml up -d

# View logs
docker compose -f docker/local/docker-compose.yml logs -f api

# Stop services
docker compose -f docker/local/docker-compose.yml down
```

---

## 🛠️ Available Scripts

| Script | Description |
|--------|-------------|
| `./scripts/setup.sh` | Create venv, install dependencies, configure git hooks |
| `./scripts/run.sh` | Start development server |
| `./scripts/test.sh` | Run tests with coverage |
| `./scripts/terraform.sh` | Execute terraform commands |
| `./scripts/migrate.sh` | Database migrations (Alembic) |

### Migration Examples

```bash
# Generate a new migration
./scripts/migrate.sh generate "add users table"

# Apply all pending migrations
./scripts/migrate.sh upgrade

# Rollback one migration
./scripts/migrate.sh downgrade

# Check migration status
./scripts/migrate.sh current
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=src --cov-report=html --cov-fail-under=80

# Run specific test file
pytest tests/unit/domain/test_user.py -v
```

### Test Structure

```python
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post("/api/v1/users", json={"email": "test@example.com"})
    assert response.status_code == 201
```

---

## 🔐 Authentication

JWT-based authentication with access and refresh tokens:

```python
from fastapi import Depends
from infrastructure.api.auth import get_current_user

@router.get("/profile")
async def get_profile(user: dict = Depends(get_current_user)):
    return user
```

| Token | Expiration | Purpose |
|-------|------------|---------|
| Access Token | 15 minutes | API requests |
| Refresh Token | 7 days | Token renewal |

---

## 🗄️ Database Support

| Database | Use Case | Connection |
|----------|----------|------------|
| Aurora PostgreSQL | Primary transactional | `postgresql+asyncpg://` |
| Aurora MySQL | Transactional | `mysql+aiomysql://` |
| DynamoDB | Key-value, high throughput | boto3 / aioboto3 |
| Redis | Caching, sessions | `redis://` |
| MongoDB | Document store | `mongodb://` |
| Redshift | Analytics | `redshift+redshift_connector://` |

---

## 🤖 AI Agents (Amazon Bedrock)

Prompts are first-class citizens following hexagonal architecture:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CustomerSupportPrompt:
    system: str = """
    Role: You are a helpful customer support assistant.
    Instructions:
    - Be polite and professional
    - Provide accurate information
    """
    
    user_template: str = "Customer query: {query}"
```

---

## 🔄 CI/CD Pipeline

### Pull Request to `staging` / `dev`
- ✅ Code quality checks (black, flake8, isort)
- ✅ Unit tests with 80% coverage
- ✅ Docker image build for QA
- ✅ Migration check (`alembic check`)

### Pull Request to `main`
- ✅ All QA checks
- ✅ Docker image build for production
- ✅ `terraform plan` (blocks merge on failure)
- 🔘 Manual trigger: `terraform apply`
- 🔘 Manual trigger: `alembic upgrade head`

---

## ⚙️ Environment Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db

# API
API_PORT=8000
DEBUG=false
LOG_LEVEL=INFO
ENVIRONMENT=local

# Authentication
JWT_SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# AWS
AWS_REGION=us-east-1
```

---

## 📝 Code Standards

- **Language**: English (code, comments, documentation)
- **Line length**: 120 characters
- **Indentation**: 4 spaces
- **Quotes**: Double quotes (`"`)
- **Naming**: `snake_case` for variables/functions, `PascalCase` for classes

### Pre-commit Hooks

Automatically runs on every commit:
- `black` — Code formatting
- `flake8` — Linting
- `isort` — Import sorting

---

## 📚 Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

Each module includes a `README.md` with:
- Description and purpose
- Business rules
- Dependencies
- Usage examples

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <sub>Built with ❤️ for developers who want to focus on code, not infrastructure.</sub>
</p>
