#!/bin/bash
# Run script for Tardigrade development server
# Starts the FastAPI application with hot reload

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default values
HOST="${API_HOST:-0.0.0.0}"
PORT="${API_PORT:-8000}"
RELOAD="--reload"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --no-reload)
            RELOAD=""
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --host HOST      Host to bind to (default: 0.0.0.0)"
            echo "  --port PORT      Port to bind to (default: 8000)"
            echo "  --no-reload      Disable auto-reload"
            echo "  -h, --help       Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Load environment variables from .env if it exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

echo "=== Starting Tardigrade Development Server ==="
echo "Host: $HOST"
echo "Port: $PORT"
echo "Reload: ${RELOAD:-disabled}"
echo ""

cd "$PROJECT_ROOT"

# Run the FastAPI application
uvicorn src.main:app --host "$HOST" --port "$PORT" $RELOAD
