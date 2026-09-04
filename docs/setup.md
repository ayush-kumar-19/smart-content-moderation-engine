# Setup Guide

## Smart Content Moderation Engine

This guide describes the AWS resources and configuration required to set up the Smart Content Moderation Engine.

## Prerequisites

The project requires:

- An AWS account
- Access to AWS Management Console
- Permission to create and configure Lambda, API Gateway, DynamoDB, SNS, IAM, Rekognition, and CloudWatch resources
- A GitHub account for source-code management
- A Discord server/channel with a webhook for moderator notifications

## AWS Region

All core AWS resources are deployed in:

```text
ap-south-1
```

AWS Region:

```text
Asia Pacific (Mumbai)
```

## 1. Create DynamoDB Table

Create a DynamoDB table with the following configuration:

| Setting | Value |
|---|---|
| Table name | `ModerationLogs` |
| Partition key | `requestId` |
| Partition key type | String |
| Sort key | None |
| Capacity mode | On-demand |
| Region | `ap-south-1` |

The table stores the moderation audit records.

## 2. Create SNS Topic

Create an SNS topic:

```text
content-moderation-alerts
```

Configuration:

- Type: Standard
- Region: `ap-south-1`

Create an email subscription to the topic and confirm the subscription using the confirmation email.

## 3. Configure Discord Webhook

Create a Discord channel for moderation alerts.

Example:

```text
#moderation-alerts
```

Create a Discord webhook for the channel.

The webhook URL should be treated as a secret and should not be committed to GitHub.

## 4. Configure IAM Role

Create an IAM role for the Lambda function.

Role name:

```text
SmartContentModerationLambdaRole
```

Attach the AWS managed policy:

```text
AWSLambdaBasicExecutionRole
```

The role also requires permissions for:

```text
rekognition:DetectModerationLabels
dynamodb:PutItem
sns:Publish
```

The permissions should be restricted to the required DynamoDB table and SNS topic.

## 5. Create Lambda Function

Create a Lambda function with:

| Setting | Value |
|---|---|
| Function name | `SmartContentModerationFunction` |
| Runtime | Python 3.14 |
| Architecture | x86_64 |
| Memory | 256 MB |
| Timeout | 30 seconds |
| Region | `ap-south-1` |
| Execution role | `SmartContentModerationLambdaRole` |

Upload the application code from:

```text
lambda/lambda_function.py
```

## 6. Configure Lambda Environment Variables

Configure the following environment variables:

```text
TABLE_NAME=ModerationLogs
SNS_TOPIC_ARN=<SNS topic ARN>
DISCORD_WEBHOOK_URL=<Discord webhook URL>
```

Do not commit the actual Discord webhook URL to GitHub.

## 7. Configure Amazon Rekognition

No model deployment is required for the standard moderation API.

The Lambda function uses:

```text
DetectModerationLabels
```

to analyze submitted images.

## 8. Create API Gateway

Create an HTTP API with:

```text
API name:
SmartContentModeration
```

Create the route:

```text
POST /moderate
```

Integrate the route with:

```text
SmartContentModerationFunction
```

Use payload format:

```text
2.0
```

Enable automatic deployment using the `$default` stage.

## 9. API Endpoint

The deployed API endpoint is:

```text
https://hls7qob2vf.execute-api.ap-south-1.amazonaws.com/moderate
```

Clients send image URLs to this endpoint.

## 10. CloudWatch Logs

AWS Lambda automatically creates CloudWatch Logs for the function.

Use CloudWatch Logs to inspect:

- Request processing
- Moderation results
- Errors
- DynamoDB writes
- SNS notification status
- Discord notification status

## 11. GitHub Repository

The source code is maintained in the GitHub repository:

```text
smart-content-moderation-engine
```

Repository structure:

```text
smart-content-moderation-engine/
├── README.md
├── LICENSE
├── .gitignore
├── lambda/
│   └── lambda_function.py
├── tests/
├── api/
├── architecture/
├── docs/
└── screenshots/
```

## 12. Security Configuration

Follow these practices during setup:

- Use an IAM role instead of AWS access keys inside Lambda.
- Grant Lambda only the permissions it requires.
- Store the Discord webhook as an environment variable.
- Never commit webhook URLs, passwords, access keys, or other secrets to GitHub.
- Keep DynamoDB and SNS permissions restricted to the required resources.
- Use HTTPS for API requests.

## Setup Complete

After completing the configuration, the expected architecture is:

```text
Client
   |
   v
API Gateway
   |
   v
Lambda
   |
   +------> Rekognition
   |
   +------> DynamoDB
   |
   +------> SNS ------> Email
   |
   +------> Discord
```

