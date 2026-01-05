# Infrastructure Guidelines

## Directory Structure

```
terraform/
├── local/        # Local development configuration
├── qa/           # QA environment
└── production/   # Production environment

docker/
├── local/        # Local Docker configuration
├── qa/           # QA Docker configuration
└── production/   # Production Docker configuration
```

## Terraform Organization

Organize Terraform files by AWS service for clarity:
- `main.tf` - Provider and backend configuration
- `variables.tf` - Input variables
- `outputs.tf` - Output values
- `vpc.tf` - VPC and networking
- `ecs.tf` - ECS cluster and services
- `rds.tf` - Database resources
- `iam.tf` - IAM roles and policies
- `secrets.tf` - Secrets Manager resources
- `dynamodb.tf` - DynamoDB tables
- `elasticache.tf` - Redis clusters
- `documentdb.tf` - MongoDB-compatible clusters (if using DocumentDB)
- `cloudwatch.tf` - CloudWatch log groups and alarms
- `bedrock.tf` - Bedrock model access and agent configuration

## CloudWatch Logs

Production environments use CloudWatch for centralized logging:
- Log group naming: `/tardigrade/{environment}/{service}`
- Retention: 30 days for production, 7 days for QA
- Logs are JSON formatted (structlog) for Logs Insights queries

## Environment Variables

Use environment variables for:
- AWS credentials (commented OIDC alternative)
- Database connection strings
- API keys and secrets
- Environment-specific configurations
