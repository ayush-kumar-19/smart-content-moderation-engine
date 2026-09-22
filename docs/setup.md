# Setup Guide

## AWS Region

The project was deployed in:

```text
ap-south-1
```

## Required AWS Services

- AWS Lambda
- Amazon API Gateway
- Amazon Rekognition
- Amazon DynamoDB
- Amazon SNS
- Amazon S3
- Amazon CloudWatch
- AWS IAM

## DynamoDB

Table:

```text
ModerationLogs
```

Partition key:

```text
requestId
```

## SNS

Topic:

```text
content-moderation-alerts
```

Subscribe and confirm the required email address.

Lambda uses:

```text
SNS_TOPIC_ARN
```

## IAM

Lambda execution role:

```text
SmartContentModerationLambdaRole
```

The role provides permissions for Rekognition, DynamoDB, SNS, and CloudWatch Logs.

## Lambda

Function:

```text
SmartContentModerationFunction
```

Runtime:

```text
Python 3.14
```

Architecture:

```text
x86_64
```

Memory:

```text
256 MB
```

Timeout:

```text
30 seconds
```

## Lambda Environment Variables

```text
TABLE_NAME
SNS_TOPIC_ARN
DISCORD_WEBHOOK_URL
```

## API Gateway

HTTP API:

```text
SmartContentModeration
```

Route:

```text
POST /moderate
```

Payload format:

```text
2.0
```

Integration:

```text
AWS Lambda
```

## Frontend

Frontend files:

```text
frontend/
├── index.html
├── style.css
└── script.js
```

The frontend is hosted using Amazon S3 Static Website Hosting and supports:

- Image URL moderation
- Laptop image upload
- Base64 image submission
- Moderation result display
- Flagged-content information

## S3 Frontend Deployment

Example bucket naming:

```text
smart-content-moderation-frontend-<AWS_ACCOUNT_ID>
```

Upload:

```bash
aws s3 sync frontend s3://YOUR-FRONTEND-BUCKET-NAME
```

The repository contains:

```text
bucket-policy.example.json
```

Replace the placeholder bucket name with the actual bucket name before applying the policy.

## GitHub Structure

```text
smart-content-moderation-engine/
├── README.md
├── LICENSE
├── .gitignore
├── bucket-policy.example.json
├── lambda/
├── frontend/
├── tests/
├── api/
├── architecture/
├── docs/
└── screenshots/
```

## Production Recommendation

The current academic deployment uses the S3 static website endpoint.

For production:

```text
Amazon S3
    ↓
Amazon CloudFront
    ↓
HTTPS
    ↓
Users
```

Prefer a private S3 bucket with CloudFront Origin Access Control.

## Security Practice

Never commit:

- AWS access keys
- AWS secret keys
- Discord webhook URLs
- API secrets
- Private credentials
- Local environment files

Only example configuration files containing placeholders should be committed.
