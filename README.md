# Smart Content Moderation Engine

An event-driven serverless image content moderation system built using AWS Lambda, Amazon Rekognition, Amazon API Gateway, Amazon DynamoDB, Amazon SNS, and Discord.

## Overview

The Smart Content Moderation Engine automatically analyzes user-submitted images and identifies potentially unsafe or policy-violating content.

The system receives an image URL through an HTTP API, downloads the image, sends it to Amazon Rekognition for moderation analysis, determines the moderation verdict and severity, stores an audit record in DynamoDB, and sends notifications when unsafe content is detected.

## Key Features

- Image moderation through a REST API
- Serverless processing using AWS Lambda
- Image analysis using Amazon Rekognition
- Automatic APPROVED or FLAGGED decision
- HIGH, MEDIUM, and LOW severity classification
- Moderation audit logs stored in DynamoDB
- Email alerts using Amazon SNS
- Discord alerts for moderators
- CloudWatch logging and monitoring
- Event-driven serverless architecture

## Architecture

```text
                         Client
                           |
                           | HTTPS POST /moderate
                           v
                   Amazon API Gateway
                           |
                           v
                    AWS Lambda
                           |
                           v
                 Amazon Rekognition
                           |
                    Moderation Result
                           |
              +------------+------------+
              |                         |
              v                         v
       Amazon DynamoDB             Amazon SNS
         Audit Log                    |
                                      +------> Email
                                      |
                                      +------> Discord
```

## Processing Flow

1. Client sends an image URL to the `/moderate` API.
2. Amazon API Gateway receives the request.
3. API Gateway invokes the AWS Lambda function.
4. Lambda validates the request.
5. Lambda downloads the image.
6. Lambda sends the image to Amazon Rekognition.
7. Rekognition returns moderation labels and confidence scores.
8. Lambda determines the moderation verdict and severity.
9. The result is stored in Amazon DynamoDB.
10. If unsafe content is detected, Lambda sends an SNS alert.
11. SNS delivers the alert through email.
12. Lambda sends a Discord notification.
13. Lambda returns the moderation result to the API client.

## AWS Services Used

| AWS Service | Purpose |
|---|---|
| Amazon API Gateway | Provides the HTTP API endpoint |
| AWS Lambda | Executes the moderation workflow |
| Amazon Rekognition | Detects potentially unsafe image content |
| Amazon DynamoDB | Stores moderation audit records |
| Amazon SNS | Sends email notifications |
| Amazon CloudWatch | Stores Lambda execution logs |

### External Service

| Service | Purpose |
|---|---|
| Discord | Receives moderation alerts through a webhook |

## API

### Endpoint

```text
POST /moderate
```

### Request Header

```text
Content-Type: application/json
```

### Request Body

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### Approved Response

```json
{
  "requestId": "UUID",
  "verdict": "APPROVED",
  "labels": [],
  "message": "No policy violations detected"
}
```

### Flagged Response

```json
{
  "requestId": "UUID",
  "verdict": "FLAGGED",
  "severity": "HIGH",
  "labels": [
    {
      "name": "Weapons",
      "confidence": 99.95
    }
  ],
  "message": "Potentially unsafe content detected"
}
```

## Moderation Severity

The system uses the confidence score returned by Amazon Rekognition to determine severity.

| Confidence Score | Severity |
|---|---|
| 90 or higher | HIGH |
| 70 to less than 90 | MEDIUM |
| Less than 70 | LOW |

A potentially unsafe moderation label results in a `FLAGGED` verdict.

## DynamoDB Audit Log

### Table

```text
ModerationLogs
```

### Partition Key

```text
requestId
```

### Stored Information

Each moderation request can contain:

- `requestId`
- `imageUrl`
- `timestamp`
- `verdict`
- `severity`
- `labels`
- `confidence`
- `notificationStatus`

Example record:

```json
{
  "requestId": "example-request-id",
  "imageUrl": "https://example.com/image.jpg",
  "timestamp": "2026-09-04T10:30:00Z",
  "verdict": "FLAGGED",
  "severity": "HIGH",
  "labels": [
    "Weapons",
    "Violence"
  ],
  "confidence": 99.95,
  "notificationStatus": "SNS_SENT,DISCORD_SENT"
}
```

## Notification System

When potentially unsafe content is detected:

```text
                    AWS Lambda
                        |
              +---------+---------+
              |                   |
              v                   v
        Amazon SNS          Discord Webhook
              |
              v
            Email
```

## Monitoring

AWS Lambda execution logs are available through Amazon CloudWatch.

The application records important processing events such as:

```text
REQUEST_RECEIVED
IMAGE_DOWNLOAD_STARTED
IMAGE_DOWNLOAD_COMPLETED
REKOGNITION_STARTED
REKOGNITION_COMPLETED
MODERATION_RESULT
DYNAMODB_WRITE
SNS_NOTIFICATION_SENT
DISCORD_NOTIFICATION_SENT
REQUEST_COMPLETED
```

## Error Handling

The system handles common failure cases including:

- Missing image URL
- Invalid request data
- Invalid image URL
- Image download failure
- Unsupported image
- Amazon Rekognition errors
- DynamoDB write errors
- SNS notification errors
- Discord notification errors

## Project Structure

```text
smart-content-moderation-engine/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── lambda/
│   └── lambda_function.py
│
├── api/
│   └── sample-requests.json
│
├── architecture/
│   ├── architecture-diagram.png
│   └── architecture.md
│
├── docs/
│   ├── setup.md
│   ├── api.md
│   ├── deployment.md
│   └── testing.md
│
├── tests/
│   ├── test_moderation.py
│   ├── test_validation.py
│   └── test_notifications.py
│
└── screenshots/
    ├── api-gateway.png
    ├── lambda.png
    ├── dynamodb.png
    ├── rekognition.png
    ├── sns.png
    ├── email.png
    ├── discord.png
    ├── cloudwatch.png
    ├── approved.png
    └── flagged.png
```

## AWS Configuration

### Region

```text
Asia Pacific (Mumbai)
ap-south-1
```

### Lambda Function

```text
SmartContentModerationFunction
```

### DynamoDB Table

```text
ModerationLogs
```

### SNS Topic

```text
content-moderation-alerts
```

### API Gateway

```text
SmartContentModeration
```

### API Route

```text
POST /moderate
```

## Testing

The application was tested at multiple stages of the workflow.

### Lambda Test

The Lambda function successfully processed an image and returned a moderation result.

### Rekognition Test

Amazon Rekognition successfully detected moderation labels including:

```text
Weapons
Violence
```

with a high confidence score.

### DynamoDB Test

Moderation results were successfully stored in the `ModerationLogs` table.

### SNS Test

Flagged content successfully triggered an email notification.

### Discord Test

Flagged content successfully triggered a notification in the configured Discord moderation channel.

### CloudWatch Test

Lambda execution logs successfully recorded the moderation workflow.

## End-to-End Workflow

```text
Client
  |
  | POST /moderate
  v
API Gateway
  |
  v
Lambda
  |
  v
Rekognition
  |
  +----------------------+
  |                      |
  v                      v
APPROVED               FLAGGED
  |                      |
  v                      +----> DynamoDB
DynamoDB                 |
                         +----> SNS ----> Email
                         |
                         +----> Discord
```

## Security

- AWS Lambda uses a dedicated IAM execution role.
- Lambda permissions are restricted to the AWS services required by the application.
- AWS credentials are not stored in the source code.
- Discord webhook credentials should not be committed to GitHub.
- Sensitive configuration should be stored using secure AWS configuration mechanisms.
- The project does not use AWS root access keys.

## Project Status

### MVP Completed

- [x] AWS Lambda
- [x] Amazon Rekognition
- [x] Amazon DynamoDB
- [x] Amazon SNS
- [x] Discord notification
- [x] Amazon API Gateway
- [x] Amazon CloudWatch
- [x] IAM execution role
- [x] Image moderation workflow
- [x] Audit logging
- [x] Email notification
- [x] Discord notification
- [x] End-to-end testing

## Future Enhancements

Possible future improvements include:

- Amazon S3 for image storage
- Amazon SQS for asynchronous processing
- Amazon EventBridge for event routing
- AWS Secrets Manager for webhook secrets
- Infrastructure as Code using AWS SAM or Terraform
- Authentication and authorization for the API
- Rate limiting and API usage plans
- Automated unit and integration testing
- CI/CD using GitHub Actions

## License

This project is licensed under the MIT License.

