#!/bin/bash
# Migration script for Tardigrade project
# Wrapper for Alembic database migration commands

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

# Load environment variables from .env if it exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

cd "$PROJECT_ROOT"

show_help() {
    echo "Usage: $0 COMMAND [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  generate MESSAGE    Generate a new migration with autogenerate"
    echo "  upgrade [REV]       Apply migrations (default: head)"
    echo "  downgrade [REV]     Rollback migrations (default: -1)"
    echo "  current             Show current migration version"
    echo "  history             Show migration history"
    echo "  check               Check for pending migrations"
    echo "  heads               Show current heads"
    echo "  show REV            Show migration details"
    echo "  sql REV             Preview SQL for migration"
    echo ""
    echo "Examples:"
    echo "  $0 generate \"add users table\""
    echo "  $0 upgrade                    # Apply all pending migrations"
    echo "  $0 upgrade head               # Apply all pending migrations"
    echo "  $0 downgrade                  # Rollback one migration"
    echo "  $0 downgrade -2               # Rollback two migrations"
    echo "  $0 sql head                   # Preview SQL without applying"
    echo ""
}

if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
    generate)
        if [ -z "$1" ]; then
            echo "Error: Migration message is required"
            echo "Usage: $0 generate \"migration message\""
            exit 1
        fi
        echo "Generating migration: $1"
        alembic revision --autogenerate -m "$1"
        echo ""
        echo "Migration generated. Review the migration file before applying."
        ;;
    upgrade)
        REV="${1:-head}"
        echo "Applying migrations to: $REV"
        alembic upgrade "$REV"
        echo "Migrations applied successfully."
        ;;
    downgrade)
        REV="${1:--1}"
        echo "Rolling back migrations: $REV"
        alembic downgrade "$REV"
        echo "Rollback complete."
        ;;
    current)
        echo "Current migration version:"
        alembic current
        ;;
    history)
        echo "Migration history:"
        alembic history --verbose
        ;;
    check)
        echo "Checking for pending migrations..."
        alembic check
        ;;
    heads)
        echo "Current heads:"
        alembic heads
        ;;
    show)
        if [ -z "$1" ]; then
            echo "Error: Revision is required"
            echo "Usage: $0 show REVISION"
            exit 1
        fi
        alembic show "$1"
        ;;
    sql)
        REV="${1:-head}"
        echo "SQL preview for migration to: $REV"
        echo "---"
        alembic upgrade "$REV" --sql
        ;;
    -h|--help|help)
        show_help
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
