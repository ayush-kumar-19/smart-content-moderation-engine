# Smart Content Moderation Engine

An event-driven serverless image content moderation system built using AWS Lambda, Amazon Rekognition, Amazon API Gateway, Amazon DynamoDB, Amazon SNS, and Discord.

## Features

- Accepts image URLs through a REST API
- Automatically analyzes images using Amazon Rekognition
- Detects potentially unsafe content
- Classifies moderation severity
- Stores moderation results in DynamoDB
- Sends email alerts using Amazon SNS
- Sends Discord moderation alerts
- Provides API responses with moderation results
- Uses CloudWatch for Lambda execution logs

## Architecture

```text
Client
   |
   | POST /moderate
   v
Amazon API Gateway
   |
   v
AWS Lambda
   |
   v
Amazon Rekognition
   |
   +--------------------+
   |                    |
   v                    v
DynamoDB               SNS
Audit Log                |
                          +----> Email
                          |
                          +----> Discord
AWS Services
Service	Purpose
Amazon API Gateway	Exposes the moderation API
AWS Lambda	Executes the moderation workflow
Amazon Rekognition	Detects unsafe image content
Amazon DynamoDB	Stores moderation audit records
Amazon SNS	Sends moderation alerts
Discord	Receives moderator notifications
Amazon CloudWatch	Stores Lambda execution logs
API
Endpoint
POST /moderate
Request
{
  "imageUrl": "https://example.com/image.jpg"
}
Approved Response
{
  "requestId": "UUID",
  "verdict": "APPROVED",
  "labels": [],
  "message": "No policy violations detected"
}
Flagged Response
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
Moderation Severity
Confidence	Severity
>= 90	HIGH
70 - 89.99	MEDIUM
< 70	LOW
DynamoDB

Table:

ModerationLogs

Partition Key:

requestId

Stored information includes:

Request ID
Image URL
Timestamp
Verdict
Severity
Moderation labels
Confidence score
Notification status
Notifications

When unsafe content is detected:

Lambda
   |
   +----> Amazon SNS ----> Email
   |
   +----> Discord Webhook
Monitoring

Lambda execution logs are available through Amazon CloudWatch.

Important processing events include:

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
Project Structure
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
AWS Region
Asia Pacific (Mumbai)
ap-south-1
Project Status

Completed MVP:

 AWS Lambda
 Amazon Rekognition
 DynamoDB audit logging
 SNS email notification
 Discord notification
 API Gateway
 CloudWatch logging
 End-to-end moderation workflow

