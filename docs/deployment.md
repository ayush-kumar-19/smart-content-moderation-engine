# Deployment Guide

## Final Deployment Architecture

```text
                   GitHub Repository
                          |
             +------------+------------+
             |                         |
        Backend Code               Frontend
             |                         |
          Lambda                  Amazon S3
             |                         |
        API Gateway             Static Website
             |
          Lambda
             |
      Amazon Rekognition
             |
       Decision Engine
        /           \
       /             \
  DynamoDB       Notifications
                 /          \
               SNS        Discord
                |
              Email
```

## Backend Deployment

The backend consists of:

- AWS Lambda
- Amazon API Gateway
- Amazon Rekognition
- Amazon DynamoDB
- Amazon SNS
- Amazon CloudWatch
- AWS IAM

## Lambda

Function:

```text
SmartContentModerationFunction
```

Source:

```text
lambda/lambda_function.py
```

Runtime:

```text
Python 3.14
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

## Frontend Deployment

Frontend:

```text
frontend/
```

Upload:

```bash
aws s3 sync frontend s3://YOUR-FRONTEND-BUCKET-NAME
```

The S3 bucket is configured for static website hosting.

## End-to-End Request Flow

### Image URL

```text
User
 ↓
S3 Frontend
 ↓
API Gateway
 ↓
Lambda
 ↓
Rekognition
 ↓
Decision
 ↓
DynamoDB
 ↓
Response
```

### Laptop Upload

```text
User selects image
 ↓
Browser reads image
 ↓
Base64 conversion
 ↓
S3 Frontend
 ↓
API Gateway
 ↓
Lambda
 ↓
Rekognition
 ↓
Decision
 ↓
DynamoDB
 ↓
SNS / Discord if flagged
 ↓
Frontend result
```

## Notifications

```text
Lambda
 ├──→ SNS → Email
 └──→ Discord Webhook
```

The Discord webhook is configured through:

```text
DISCORD_WEBHOOK_URL
```

## Logging

Lambda execution logs are available through Amazon CloudWatch Logs.

DynamoDB provides persistent moderation audit records.

## Deployment Verification

The completed deployment was verified through:

- Lambda execution
- Amazon Rekognition response
- DynamoDB audit record
- SNS notification
- Discord notification
- CloudWatch logs
- API Gateway request
- Frontend image URL submission
- Frontend laptop image upload

## Production Improvement

The current academic frontend uses an S3 static website endpoint.

For production:

```text
User
 ↓
CloudFront HTTPS
 ↓
Private S3 Bucket
 ↓
Frontend
 ↓
API Gateway
```

This provides HTTPS and avoids exposing the S3 bucket directly to public website traffic.
