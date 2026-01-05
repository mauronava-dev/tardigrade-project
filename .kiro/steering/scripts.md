# Project Scripts

## Available Scripts

Located in `scripts/` directory:

| Script | Purpose |
|--------|---------|
| `setup.sh` | Create venv, install dependencies, configure git hooks |
| `run.sh` | Start development server |
| `test.sh` | Run unit tests with coverage |
| `terraform.sh` | Execute terraform commands |
| `init-terraform.sh` | Initialize terraform (tech lead only, run once) |
| `migrate.sh` | Execute Alembic migration commands |

## Usage

```bash
# Initial setup
./scripts/setup.sh

# Run development server
./scripts/run.sh

# Run tests
./scripts/test.sh

# Terraform operations
./scripts/terraform.sh plan
./scripts/terraform.sh apply

# Database migrations
./scripts/migrate.sh generate "add users table"  # Generate migration
./scripts/migrate.sh upgrade                      # Apply all pending
./scripts/migrate.sh downgrade                    # Rollback one migration
./scripts/migrate.sh current                      # Show current version
./scripts/migrate.sh history                      # Show migration history
./scripts/migrate.sh check                        # Check for pending migrations
```

## Script Requirements

- All scripts must be executable (`chmod +x`)
- Include error handling and validation
- Support both macOS and Linux
- Document usage in script header comments
