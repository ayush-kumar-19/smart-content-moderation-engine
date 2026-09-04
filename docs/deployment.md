# Deployment Guide

## Smart Content Moderation Engine

This document describes the deployment process for the Smart Content Moderation Engine on AWS.

## Deployment Architecture

```text
GitHub Repository
       |
       v
Lambda Function
       |
       +----> Amazon Rekognition
       |
       +----> DynamoDB
       |
       +----> Amazon SNS
       |
       +----> Discord Webhook
       |
       v
API Gateway
```

## AWS Region

Deploy the application resources in:

```text
ap-south-1
```

## 1. Deploy Lambda Code

The Lambda application code is located at:

```text
lambda/lambda_function.py
```

The deployed Lambda function is:

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

## 2. Configure Lambda Environment Variables

The Lambda function requires:

```text
TABLE_NAME=ModerationLogs
SNS_TOPIC_ARN=<SNS topic ARN>
DISCORD_WEBHOOK_URL=<Discord webhook URL>
```

The actual Discord webhook URL must not be stored in source code or committed to GitHub.

## 3. Configure Lambda IAM Role

Lambda uses:

```text
SmartContentModerationLambdaRole
```

Required permissions include:

```text
rekognition:DetectModerationLabels
dynamodb:PutItem
sns:Publish
```

CloudWatch logging is provided through:

```text
AWSLambdaBasicExecutionRole
```

## 4. Deploy API Gateway

The HTTP API is:

```text
SmartContentModeration
```

Route:

```text
POST /moderate
```

Integration:

```text
SmartContentModerationFunction
```

Payload format:

```text
2.0
```

Stage:

```text
$default
```

## 5. API Endpoint

The deployed endpoint is:

```text
https://hls7qob2vf.execute-api.ap-south-1.amazonaws.com/moderate
```

## 6. DynamoDB Configuration

The deployed DynamoDB table is:

```text
ModerationLogs
```

Partition key:

```text
requestId
```

The table uses on-demand capacity.

## 7. SNS Configuration

The SNS topic is:

```text
content-moderation-alerts
```

The confirmed email subscription receives alerts when content is flagged.

## 8. Discord Configuration

Flagged-content notifications are sent to the configured Discord moderation channel through the webhook.

The webhook is supplied to Lambda through the environment variable:

```text
DISCORD_WEBHOOK_URL
```

## 9. Deployment Verification

After deployment, verify the following:

### Lambda

Confirm that:

```text
SmartContentModerationFunction
```

is active and has the correct environment variables.

### API Gateway

Confirm that:

```text
POST /moderate
```

is deployed and connected to Lambda.

### DynamoDB

Confirm that:

```text
ModerationLogs
```

exists and accepts moderation records.

### SNS

Confirm that:

```text
content-moderation-alerts
```

has a confirmed email subscription.

### Discord

Confirm that the moderation webhook is configured.

### CloudWatch

Confirm that Lambda execution logs are available.

## 10. Source Code Deployment

The source code is maintained in GitHub.

Repository:

```text
smart-content-moderation-engine
```

Important files:

```text
lambda/lambda_function.py
README.md
architecture/architecture.md
docs/api.md
docs/setup.md
```

After changing application code:

```text
1. Update lambda/lambda_function.py
2. Test the code
3. Deploy the updated Lambda code
4. Verify CloudWatch logs
5. Commit changes to GitHub
6. Push changes to the main branch
```

## 11. Production Deployment Improvements

For a production environment, the deployment can be improved using Infrastructure as Code.

Possible options:

- AWS SAM
- Terraform
- AWS CloudFormation

Additional production components may include:

- Amazon S3
- Amazon SQS
- Amazon EventBridge
- AWS Secrets Manager
- AWS WAF
- CloudWatch alarms
- API authentication

## Deployment Complete

The deployed system provides:

```text
HTTPS API
    |
    v
API Gateway
    |
    v
Lambda
    |
    +----> Rekognition
    |
    +----> DynamoDB
    |
    +----> SNS ----> Email
    |
    +----> Discord
```

