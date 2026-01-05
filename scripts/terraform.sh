#!/bin/bash
# Terraform script for Tardigrade project
# Wrapper for terraform operations across environments

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default environment
ENVIRONMENT="${TF_ENVIRONMENT:-local}"

show_help() {
    echo "Usage: $0 [OPTIONS] COMMAND"
    echo ""
    echo "Options:"
    echo "  -e, --env ENV    Environment: local, qa, production (default: local)"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Commands:"
    echo "  init             Initialize terraform"
    echo "  plan             Show execution plan"
    echo "  apply            Apply changes"
    echo "  destroy          Destroy infrastructure"
    echo "  output           Show outputs"
    echo "  validate         Validate configuration"
    echo "  fmt              Format terraform files"
    echo "  state            Show state"
    echo ""
    echo "Examples:"
    echo "  $0 plan                      # Plan for local environment"
    echo "  $0 -e qa plan                # Plan for QA environment"
    echo "  $0 -e production apply       # Apply to production"
    echo ""
}

# Parse options
while [[ $# -gt 0 ]]; do
    case $1 in
        -e|--env)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            break
            ;;
    esac
done

# Validate environment
case "$ENVIRONMENT" in
    local|qa|production)
        ;;
    *)
        echo "Error: Invalid environment '$ENVIRONMENT'"
        echo "Valid environments: local, qa, production"
        exit 1
        ;;
esac

TF_DIR="$PROJECT_ROOT/terraform/$ENVIRONMENT"

# Check if terraform directory exists
if [ ! -d "$TF_DIR" ]; then
    echo "Error: Terraform directory not found: $TF_DIR"
    exit 1
fi

# Load environment variables from .env if it exists
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(grep -v '^#' "$PROJECT_ROOT/.env" | xargs)
fi

if [ $# -eq 0 ]; then
    show_help
    exit 1
fi

COMMAND="$1"
shift

echo "=== Terraform: $ENVIRONMENT ==="
echo "Directory: $TF_DIR"
echo ""

cd "$TF_DIR"

case "$COMMAND" in
    init)
        echo "Initializing terraform..."
        terraform init "$@"
        ;;
    plan)
        echo "Creating execution plan..."
        terraform plan "$@"
        ;;
    apply)
        echo "Applying changes..."
        if [ "$ENVIRONMENT" = "production" ]; then
            echo "WARNING: You are about to apply changes to PRODUCTION"
            read -p "Are you sure? (yes/no): " confirm
            if [ "$confirm" != "yes" ]; then
                echo "Aborted."
                exit 1
            fi
        fi
        terraform apply "$@"
        ;;
    destroy)
        echo "Destroying infrastructure..."
        if [ "$ENVIRONMENT" = "production" ]; then
            echo "WARNING: You are about to DESTROY PRODUCTION infrastructure"
            read -p "Type 'destroy production' to confirm: " confirm
            if [ "$confirm" != "destroy production" ]; then
                echo "Aborted."
                exit 1
            fi
        fi
        terraform destroy "$@"
        ;;
    output)
        terraform output "$@"
        ;;
    validate)
        echo "Validating configuration..."
        terraform validate "$@"
        ;;
    fmt)
        echo "Formatting terraform files..."
        terraform fmt -recursive "$PROJECT_ROOT/terraform"
        ;;
    state)
        terraform state "$@"
        ;;
    *)
        echo "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
