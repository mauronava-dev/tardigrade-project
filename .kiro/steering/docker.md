# Docker Guidelines

## Directory Structure

```
docker/
├── local/
│   ├── Dockerfile
│   └── docker-compose.yml    # App + PostgreSQL + Redis
├── qa/
│   ├── Dockerfile
│   └── docker-compose.yml    # App only (uses AWS services)
└── production/
    └── Dockerfile            # Optimized for ECS/Fargate
```

## Local Development

```bash
# Start all services
docker compose -f docker/local/docker-compose.yml up -d

# View logs
docker compose -f docker/local/docker-compose.yml logs -f api

# Stop services
docker compose -f docker/local/docker-compose.yml down

# Rebuild after dependency changes
docker compose -f docker/local/docker-compose.yml build --no-cache
```

## Environment-Specific Dockerfiles

### Local (development)
- Hot reload enabled
- Debug tools included
- Mounts source code as volume

### QA
- Production-like build
- No debug tools
- Environment variables from AWS

### Production
- Multi-stage build (minimal image)
- Non-root user
- Health check included
- Optimized for ECS/Fargate

## Docker Compose Services (Local)

| Service | Port | Purpose |
|---------|------|---------|
| api | 8000 | FastAPI application |
| postgres | 5432 | Aurora PostgreSQL (local) |
| redis | 6379 | Redis cache |
| mongo | 27017 | MongoDB (optional) |

## Build Commands

```bash
# Build for specific environment
docker build -f docker/local/Dockerfile -t app:local .
docker build -f docker/qa/Dockerfile -t app:qa .
docker build -f docker/production/Dockerfile -t app:prod .
```
