# System Architecture

## Smart Content Moderation Engine

The Smart Content Moderation Engine is a serverless, event-driven application that automatically analyzes submitted images for potentially unsafe content.

## Architecture Diagram

```text
                         +----------------+
                         |     Client     |
                         +-------+--------+
                                 |
                                 | HTTPS POST
                                 | /moderate
                                 v
                     +-----------------------+
                     |   Amazon API Gateway  |
                     +-----------+-----------+
                                 |
                                 | Invoke
                                 v
                     +-----------------------+
                     |      AWS Lambda       |
                     | SmartContentModeration|
                     +-----------+-----------+
                                 |
                                 | Image Bytes
                                 v
                     +-----------------------+
                     |  Amazon Rekognition   |
                     | DetectModerationLabels|
                     +-----------+-----------+
                                 |
                                 | Moderation Result
                                 v
                     +-----------------------+
                     |   Decision Engine     |
                     | APPROVED / FLAGGED    |
                     | Severity Calculation  |
                     +-----------+-----------+
                                 |
                    +------------+------------+
                    |                         |
                    v                         v
          +-------------------+       +-------------------+
          | Amazon DynamoDB   |       |   Notification    |
          |   ModerationLogs  |       |     System        |
          +-------------------+       +---------+---------+
                                                |
                                      +---------+---------+
                                      |                   |
                                      v                   v
                              +-------------+     +-------------+
                              | Amazon SNS  |     |   Discord   |
                              +------+------+     +-------------+
                                     |
                                     v
                                  Email
```

## Components

### 1. Client

The client submits an image URL to the moderation API using an HTTPS POST request.

Example:

```http
POST /moderate
Content-Type: application/json
```

Request body:

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### 2. Amazon API Gateway

Amazon API Gateway provides the public HTTPS endpoint for the application.

Configuration:

- API type: HTTP API
- API name: `SmartContentModeration`
- Route: `POST /moderate`
- Integration: AWS Lambda
- Region: `ap-south-1`

API Gateway forwards the request to the Lambda function.

### 3. AWS Lambda

The Lambda function contains the main application logic.

Function:

`SmartContentModerationFunction`

Responsibilities:

1. Receive the API request.
2. Validate the image URL.
3. Download the image.
4. Send the image bytes to Amazon Rekognition.
5. Analyze moderation labels.
6. Determine whether the image is approved or flagged.
7. Calculate severity.
8. Store the audit record in DynamoDB.
9. Send notifications for flagged content.
10. Return the moderation result to the client.

### 4. Amazon Rekognition

Amazon Rekognition performs image moderation using the `DetectModerationLabels` API.

The service identifies potentially unsafe content and returns moderation labels with confidence scores.

The Lambda function uses these results to determine the moderation decision.

### 5. Decision Engine

The decision engine processes the Rekognition response.

Decision rules:

```text
No moderation labels
        |
        v
    APPROVED
```

```text
Moderation label >= 70%
        |
        v
     FLAGGED
```

Severity calculation:

```text
Confidence >= 90%  -> HIGH
Confidence >= 70%  -> MEDIUM
Confidence < 70%   -> LOW
```

The current implementation uses a minimum moderation confidence threshold of 70%.

### 6. Amazon DynamoDB

DynamoDB stores the moderation audit trail.

Table:

`ModerationLogs`

Partition key:

`requestId`

Stored information includes:

- Request ID
- Image URL
- Timestamp
- Moderation decision
- Severity
- Detected labels
- Confidence scores
- Processing information

This provides a persistent record of moderation requests.

### 7. Amazon SNS

Amazon SNS is used for human moderator notifications.

Topic:

`content-moderation-alerts`

When an image is flagged:

```text
Lambda
   |
   v
SNS Topic
   |
   v
Email Notification
```

### 8. Discord

The Lambda function also sends flagged-content notifications to a Discord moderation channel through a Discord webhook.

Notification flow:

```text
Lambda
   |
   v
Discord Webhook
   |
   v
#moderation-alerts
```

The Discord webhook URL is stored as a Lambda environment variable rather than directly in the source code.

### 9. Amazon CloudWatch

AWS Lambda automatically sends execution logs to Amazon CloudWatch Logs.

CloudWatch is used to monitor:

- Lambda execution
- Request IDs
- Moderation decisions
- Detected labels
- Processing errors
- Notification status

## Complete Request Flow

```text
1. Client submits image URL
             |
             v
2. API Gateway receives POST /moderate
             |
             v
3. Lambda function is invoked
             |
             v
4. Lambda validates the URL
             |
             v
5. Lambda downloads image
             |
             v
6. Image is sent to Amazon Rekognition
             |
             v
7. Rekognition returns moderation labels
             |
             v
8. Decision engine calculates:
      APPROVED / FLAGGED
      LOW / MEDIUM / HIGH
             |
             +----------------------+
             |                      |
             v                      v
      DynamoDB audit log      If FLAGGED
                                    |
                                    v
                              SNS + Discord
                                    |
                                    v
                              Human Moderator
             |
             v
9. API returns JSON response
```

## AWS Region

The project resources are deployed in:

`ap-south-1`

AWS Region:

`Asia Pacific (Mumbai)`

## Design Characteristics

### Serverless

The application uses AWS Lambda and API Gateway, eliminating the need to manage traditional servers.

### Event-Driven

The moderation workflow is triggered by an HTTP request and automatically invokes the required AWS services.

### Scalable

AWS managed services can scale according to workload without requiring manual server provisioning.

### Pay-as-You-Go

The architecture primarily uses managed AWS services that charge according to usage.

### Automated Moderation

Amazon Rekognition performs automated image content analysis.

### Human-in-the-Loop

Flagged content generates notifications for human moderators.

### Auditable

DynamoDB stores moderation results and request information for later review.

## Security

The application follows basic cloud security practices:

- Lambda uses an IAM execution role.
- Permissions are restricted to required AWS services.
- The Discord webhook is stored as an environment variable.
- Secrets are not stored in the GitHub repository.
- DynamoDB access is limited to the required table.
- SNS publishing is limited to the moderation alert topic.
- Rekognition access is limited to the moderation API.

## Future Enhancements

Possible production improvements include:

- Amazon S3 for direct image uploads.
- Amazon SQS for asynchronous processing.
- Amazon EventBridge for event-driven workflows.
- AWS Secrets Manager for webhook credentials.
- Amazon CloudWatch alarms and dashboards.
- AWS WAF for API protection.
- Infrastructure as Code using AWS SAM or Terraform.
- Authentication and authorization for API clients.
- Dead-letter queues for failed processing.
- Additional moderation categories and custom business rules.

