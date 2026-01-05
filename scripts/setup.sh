#!/bin/bash
# Setup script for Tardigrade project
# Creates virtual environment and installs dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Tardigrade Project Setup ==="

# Check Python version
PYTHON_CMD=""
if command -v python3.12 &> /dev/null; then
    PYTHON_CMD="python3.12"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "Error: Python 3 is required but not found"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version

# Create virtual environment
VENV_DIR="$PROJECT_ROOT/venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing project dependencies..."
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "Installing development dependencies..."
pip install -r "$PROJECT_ROOT/requirements-dev.txt"

# Create .env file from example if it doesn't exist
if [ ! -f "$PROJECT_ROOT/.env" ] && [ -f "$PROJECT_ROOT/.env.example" ]; then
    echo "Creating .env file from .env.example..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
fi

# Setup git hooks (pre-commit)
if [ -d "$PROJECT_ROOT/.git" ]; then
    echo "Setting up git hooks..."
    PRE_COMMIT_HOOK="$PROJECT_ROOT/.git/hooks/pre-commit"
    cat > "$PRE_COMMIT_HOOK" << 'EOF'
#!/bin/bash
# Pre-commit hook for code quality checks

set -e

echo "Running pre-commit checks..."

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run black
echo "Running black..."
black --check .

# Run isort
echo "Running isort..."
isort --check-only .

# Run flake8
echo "Running flake8..."
flake8 .

echo "All pre-commit checks passed!"
EOF
    chmod +x "$PRE_COMMIT_HOOK"
    echo "Git pre-commit hook installed"
fi

echo ""
echo "=== Setup Complete ==="
echo "To activate the virtual environment, run:"
echo "  source venv/bin/activate"
