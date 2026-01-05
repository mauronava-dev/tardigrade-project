# CI/CD Secrets and Variables Configuration

This document describes the required secrets and variables for the CI/CD pipelines in both GitHub Actions and GitLab CI.

## Table of Contents

- [GitHub Actions Configuration](#github-actions-configuration)
  - [Required Secrets](#github-actions-required-secrets)
  - [Environment Protection Setup](#github-actions-environment-protection)
  - [OIDC Configuration](#github-actions-oidc-configuration)
- [GitLab CI Configuration](#gitlab-ci-configuration)
  - [Required Variables](#gitlab-ci-required-variables)
  - [Protected Branch Settings](#gitlab-ci-protected-branch-settings)
  - [OIDC Configuration](#gitlab-ci-oidc-configuration)
- [AWS IAM Role Configuration](#aws-iam-role-configuration)
- [Security Best Practices](#security-best-practices)

---

## GitHub Actions Configuration

### GitHub Actions Required Secrets

Configure these secrets in your GitHub repository under **Settings > Secrets and variables > Actions**.

#### AWS Authentication Secrets (OIDC - Recommended)

| Secret Name         | Description                                                 | Required | Environment |
| ------------------- | ----------------------------------------------------------- | -------- | ----------- |
| `AWS_ROLE_ARN_QA`   | IAM role ARN for QA environment OIDC authentication         | Yes      | QA          |
| `AWS_ROLE_ARN_PROD` | IAM role ARN for Production environment OIDC authentication | Yes      | Production  |

#### AWS Authentication Secrets (Static Credentials - Fallback)

> **Note**: Only use static credentials if OIDC is not configured. Uncomment the relevant sections in workflow files.

| Secret Name             | Description           | Required | Environment |
| ----------------------- | --------------------- | -------- | ----------- |
| `AWS_ACCESS_KEY_ID`     | AWS access key ID     | Fallback | All         |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | Fallback | All         |

#### Database Secrets

| Secret Name         | Description                                           | Required             | Environment |
| ------------------- | ----------------------------------------------------- | -------------------- | ----------- |
| `DATABASE_URL_QA`   | Database connection string for QA environment         | Yes (for migrations) | QA          |
| `DATABASE_URL_PROD` | Database connection string for Production environment | Yes (for migrations) | Production  |

### GitHub Actions Environment Protection

Configure environment protection rules under **Settings > Environments**.

#### QA Environment

1. Navigate to **Settings > Environments > New environment**
2. Name: `qa`
3. Configure protection rules:
   - **Required reviewers**: Optional (recommended for migration jobs)
   - **Wait timer**: Optional
   - **Deployment branches**: Limit to `staging` and `dev` branches

#### Production Environment

1. Navigate to **Settings > Environments > New environment**
2. Name: `production`
3. Configure protection rules:
   - **Required reviewers**: Enable and add designated reviewers (DevOps team, Tech Lead)
   - **Wait timer**: Optional (e.g., 5 minutes for review)
   - **Deployment branches**: Limit to `main` branch only

**Protected Jobs in Production:**

- `terraform-apply` - Requires manual approval
- `alembic-upgrade` - Requires manual approval
- `alembic-downgrade` - Requires manual approval (emergency only)

### GitHub Actions OIDC Configuration

To use OIDC authentication with AWS:

1. **Create an OIDC Identity Provider in AWS IAM**:
   - Provider URL: `https://token.actions.githubusercontent.com`
   - Audience: `sts.amazonaws.com`

2. **Create IAM Roles** with trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<GITHUB_ORG>/<REPO_NAME>:*"
        }
      }
    }
  ]
}
```

3. **Attach Required Policies** to the IAM roles:
   - ECR push/pull permissions
   - S3 access for Terraform state
   - DynamoDB access for Terraform locks
   - Secrets Manager access (if needed)
   - RDS/Aurora access for migrations

---

## GitLab CI Configuration

### GitLab CI Required Variables

Configure these variables in your GitLab project under **Settings > CI/CD > Variables**.

#### AWS Authentication Variables (OIDC - Recommended)

| Variable Name       | Description                             | Protected | Masked | Environment Scope |
| ------------------- | --------------------------------------- | --------- | ------ | ----------------- |
| `AWS_ROLE_ARN_QA`   | IAM role ARN for QA environment         | Yes       | No     | `staging`, `dev`  |
| `AWS_ROLE_ARN_PROD` | IAM role ARN for Production environment | Yes       | No     | `production`      |
| `AWS_ACCOUNT_ID`    | AWS account ID for ECR registry         | Yes       | No     | All               |
| `AWS_REGION`        | AWS region (default: us-east-1)         | No        | No     | All               |

#### AWS Authentication Variables (Static Credentials - Fallback)

> **Note**: Only configure if OIDC is not available. Uncomment the relevant sections in `.gitlab-ci.yml`.

| Variable Name           | Description           | Protected | Masked | Environment Scope |
| ----------------------- | --------------------- | --------- | ------ | ----------------- |
| `AWS_ACCESS_KEY_ID`     | AWS access key ID     | Yes       | Yes    | All               |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | Yes       | Yes    | All               |

#### Database Variables

| Variable Name  | Description                | Protected | Masked | Environment Scope    |
| -------------- | -------------------------- | --------- | ------ | -------------------- |
| `DATABASE_URL` | Database connection string | Yes       | Yes    | Environment-specific |

### GitLab CI Protected Branch Settings

Configure protected branches under **Settings > Repository > Protected branches**.

#### Staging Branch

1. Branch: `staging`
2. Allowed to merge: Developers + Maintainers
3. Allowed to push: No one (force push disabled)
4. Require approval: 1 approval required

#### Dev Branch

1. Branch: `dev`
2. Allowed to merge: Developers + Maintainers
3. Allowed to push: Developers + Maintainers
4. Require approval: Optional

#### Main Branch (Production)

1. Branch: `main`
2. Allowed to merge: Maintainers only
3. Allowed to push: No one (force push disabled)
4. Require approval: 2 approvals required
5. Code owner approval: Required (if CODEOWNERS file exists)

### GitLab CI Protected Environments

Configure protected environments under **Settings > CI/CD > Protected environments**.

#### QA Environment

1. Environment: `qa`
2. Allowed to deploy: Developers + Maintainers
3. Required approvals: 0 (optional)

#### Production Environment

1. Environment: `production`
2. Allowed to deploy: Maintainers only
3. Required approvals: 1 (from designated approvers)
4. Approvers: Add DevOps team members

### GitLab CI OIDC Configuration

GitLab provides OIDC tokens via `CI_JOB_JWT_V2`. To configure:

1. **Create an OIDC Identity Provider in AWS IAM**:
   - Provider URL: `https://gitlab.com` (or your GitLab instance URL)
   - Audience: `https://gitlab.com` (or your GitLab instance URL)

2. **Create IAM Roles** with trust policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<AWS_ACCOUNT_ID>:oidc-provider/gitlab.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "gitlab.com:aud": "https://gitlab.com"
        },
        "StringLike": {
          "gitlab.com:sub": "project_path:<GITLAB_GROUP>/<PROJECT_NAME>:*"
        }
      }
    }
  ]
}
```

3. **Enable ID Tokens** in GitLab:
   - Go to **Settings > CI/CD > Token Access**
   - Ensure ID tokens are enabled for the project

---

## AWS IAM Role Configuration

### Required IAM Policies

Create IAM policies with the following permissions for CI/CD roles:

#### ECR Access Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["ecr:GetAuthorizationToken"],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ecr:BatchCheckLayerAvailability",
        "ecr:GetDownloadUrlForLayer",
        "ecr:BatchGetImage",
        "ecr:PutImage",
        "ecr:InitiateLayerUpload",
        "ecr:UploadLayerPart",
        "ecr:CompleteLayerUpload"
      ],
      "Resource": "arn:aws:ecr:<REGION>:<ACCOUNT_ID>:repository/tardigrade"
    }
  ]
}
```

#### Terraform State Access Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::tardigrade-terraform-state",
        "arn:aws:s3:::tardigrade-terraform-state/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:DeleteItem"],
      "Resource": "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/tardigrade-terraform-locks"
    }
  ]
}
```

### Role Separation

| Role                   | Purpose                    | Permissions                                      |
| ---------------------- | -------------------------- | ------------------------------------------------ |
| `tardigrade-cicd-qa`   | QA environment deployments | ECR, S3 (QA state), limited AWS resources        |
| `tardigrade-cicd-prod` | Production deployments     | ECR, S3 (prod state), full Terraform permissions |

---

## Security Best Practices

### Secrets Management

1. **Never commit secrets** to the repository
2. **Use OIDC** instead of static credentials when possible
3. **Rotate credentials** regularly (every 90 days for static credentials)
4. **Mask sensitive variables** in CI/CD logs
5. **Limit secret scope** to specific environments when possible

### Access Control

1. **Principle of least privilege** - Grant minimum required permissions
2. **Separate roles** for QA and Production environments
3. **Require approvals** for production deployments
4. **Audit access** regularly and remove unused permissions

### Pipeline Security

1. **Protected branches** prevent unauthorized changes
2. **Environment protection** requires approval for sensitive operations
3. **Manual triggers** for destructive operations (terraform apply, alembic downgrade)
4. **Artifact retention** limited to 7 days to reduce exposure

### Monitoring and Auditing

1. Enable **CloudTrail** for AWS API call logging
2. Enable **GitHub/GitLab audit logs** for repository access
3. Set up **alerts** for failed authentication attempts
4. Review **deployment history** regularly

---

## Quick Setup Checklist

### GitHub Actions

- [ ] Create OIDC identity provider in AWS IAM
- [ ] Create IAM roles for QA and Production
- [ ] Add `AWS_ROLE_ARN_QA` secret
- [ ] Add `AWS_ROLE_ARN_PROD` secret
- [ ] Add `DATABASE_URL_QA` secret
- [ ] Add `DATABASE_URL_PROD` secret
- [ ] Create `qa` environment with protection rules
- [ ] Create `production` environment with required reviewers
- [ ] Verify ECR repository exists

### GitLab CI

- [ ] Create OIDC identity provider in AWS IAM
- [ ] Create IAM roles for QA and Production
- [ ] Add `AWS_ROLE_ARN_QA` variable (protected)
- [ ] Add `AWS_ROLE_ARN_PROD` variable (protected)
- [ ] Add `AWS_ACCOUNT_ID` variable (protected)
- [ ] Configure protected branches (staging, dev, main)
- [ ] Configure protected environments (qa, production)
- [ ] Add required approvers for production environment
- [ ] Verify ECR repository exists
