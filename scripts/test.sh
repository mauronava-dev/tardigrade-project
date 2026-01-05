#!/bin/bash
# Test script for Tardigrade project
# Runs tests with coverage reporting

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Default values
COVERAGE_MIN=80
COVERAGE_REPORT="html"
VERBOSE=""
TEST_PATH=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --coverage-min)
            COVERAGE_MIN="$2"
            shift 2
            ;;
        --report)
            COVERAGE_REPORT="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        --unit)
            TEST_PATH="tests/unit"
            shift
            ;;
        --integration)
            TEST_PATH="tests/integration"
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS] [TEST_PATH]"
            echo ""
            echo "Options:"
            echo "  --coverage-min N   Minimum coverage percentage (default: 80)"
            echo "  --report TYPE      Coverage report type: html, xml, term (default: html)"
            echo "  -v, --verbose      Verbose output"
            echo "  --unit             Run only unit tests"
            echo "  --integration      Run only integration tests"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                           # Run all tests"
            echo "  $0 --unit                    # Run unit tests only"
            echo "  $0 tests/unit/domain         # Run specific test directory"
            echo "  $0 -v --coverage-min 90      # Verbose with 90% coverage minimum"
            exit 0
            ;;
        *)
            if [ -z "$TEST_PATH" ]; then
                TEST_PATH="$1"
            fi
            shift
            ;;
    esac
done

# Activate virtual environment if it exists
if [ -f "$PROJECT_ROOT/venv/bin/activate" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
fi

cd "$PROJECT_ROOT"

echo "=== Running Tardigrade Tests ==="
echo "Coverage minimum: ${COVERAGE_MIN}%"
echo "Report type: $COVERAGE_REPORT"
echo ""

# Build pytest command
PYTEST_CMD="pytest"

# Add coverage options
PYTEST_CMD="$PYTEST_CMD --cov=src --cov-report=$COVERAGE_REPORT --cov-fail-under=$COVERAGE_MIN"

# Add verbose flag if set
if [ -n "$VERBOSE" ]; then
    PYTEST_CMD="$PYTEST_CMD $VERBOSE"
fi

# Add test path if specified
if [ -n "$TEST_PATH" ]; then
    PYTEST_CMD="$PYTEST_CMD $TEST_PATH"
fi

echo "Running: $PYTEST_CMD"
echo ""

# Run tests
$PYTEST_CMD

echo ""
echo "=== Tests Complete ==="
if [ "$COVERAGE_REPORT" = "html" ]; then
    echo "Coverage report available at: htmlcov/index.html"
fi
