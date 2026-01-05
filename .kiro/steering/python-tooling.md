# Python Tooling Configuration

## Stack

- Python 3.12
- FastAPI for API development
- SQLAlchemy for ORM
- Alembic for database migrations
- structlog for structured logging
- Virtual environment using `venv`

## Code Formatters and Linters

### Black Configuration

```toml
[tool.black]
line-length = 120
target-version = ["py312"]
skip-string-normalization = false
```

### Flake8 Configuration

```ini
[flake8]
max-line-length = 120
extend-ignore = E203, W503
exclude = .git,__pycache__,venv,.venv,build,dist
```

### Isort Configuration

```toml
[tool.isort]
profile = "black"
line_length = 120
multi_line_output = 3
include_trailing_comma = true
force_single_line = false
```

## Pre-commit Hooks

The project uses git hooks for:
- `pre-commit`: Runs black, flake8, and isort

## Running Quality Checks

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .

# Run tests with coverage
pytest --cov=src --cov-report=html
```

## Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
