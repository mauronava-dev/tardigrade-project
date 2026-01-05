# CI/CD Guidelines

## Pipeline Triggers

### MR to `staging` or `dev`
- Code quality checks (black, flake8, isort)
- Unit tests with 80% coverage minimum
- Generate downloadable coverage report
- Build Docker image for `qa` environment
- Artifacts available for 7 days
- Run `alembic check` to detect pending migrations
- Manual trigger for `alembic upgrade head` (QA database)

### MR to `main`
- Code quality checks (black, flake8, isort)
- Unit tests with 80% coverage minimum
- Generate downloadable coverage report
- Build Docker image for `production`
- Run `terraform plan`
- Run `alembic check` to detect pending migrations
- Manual trigger for `terraform apply`
- Manual trigger for `alembic upgrade head` (production database)
- Manual trigger for `alembic downgrade -1` (rollback, emergency only)
- MR blocked if `terraform plan` fails

## Database Migration Safety

- `alembic upgrade` and `alembic downgrade` are always manual triggers
- Preview migration SQL before applying: `alembic upgrade head --sql`
- Backup database before running migrations in production
- Run migrations during low-traffic windows

## Authentication

Use OIDC for AWS deployments. Environment variable credentials should be commented but available.

## Supported Platforms
- GitLab CI (`.gitlab-ci.yml`)
- GitHub Actions (`.github/workflows/`)
