# API Documentation

## Smart Content Moderation API

The Smart Content Moderation Engine exposes an HTTP API for submitting image URLs for content moderation.

## Endpoint

**Method:** `POST`

**Route:** `/moderate`

**Full URL:**

```text
https://hls7qob2vf.execute-api.ap-south-1.amazonaws.com/moderate
```

## Request

### Headers

```http
Content-Type: application/json
```

### Request Body

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `imageUrl` | String | Yes | Publicly accessible image URL |

## Approved Response

```json
{
  "requestId": "example-request-id",
  "decision": "APPROVED",
  "severity": "LOW",
  "labels": [],
  "timestamp": "2026-08-01T10:00:00+00:00"
}
```

## Flagged Response

```json
{
  "requestId": "example-request-id",
  "decision": "FLAGGED",
  "severity": "HIGH",
  "labels": [
    {
      "name": "Weapons",
      "confidence": 99.95
    },
    {
      "name": "Violence",
      "confidence": 99.95
    }
  ],
  "timestamp": "2026-08-01T10:00:00+00:00"
}
```

## Decision Rules

| Confidence | Decision | Severity |
|---|---|---|
| No moderation labels | APPROVED | LOW |
| 70% - 89.99% | FLAGGED | MEDIUM |
| 90% or higher | FLAGGED | HIGH |

## Processing Flow

```text
Client
  |
  | POST /moderate
  | imageUrl
  v
API Gateway
  |
  v
AWS Lambda
  |
  v
Amazon Rekognition
  |
  v
Decision Engine
  |
  +------------------+
  |                  |
  v                  v
DynamoDB          If FLAGGED
                     |
                     v
                 SNS + Discord
                     |
                     v
              Human Moderator
```

## Example cURL Request

```bash
curl -X POST   "https://hls7qob2vf.execute-api.ap-south-1.amazonaws.com/moderate"   -H "Content-Type: application/json"   -d '{"imageUrl":"https://example.com/image.jpg"}'
```

## HTTP Status Codes

| Status Code | Meaning |
|---|---|
| `200` | Moderation completed successfully |
| `400` | Invalid request or image URL |
| `500` | Internal processing error |

## Validation

The Lambda function validates the submitted image URL before downloading the image.

The application also limits the downloaded image size to prevent unnecessarily large requests.

## Audit Logging

Every successfully processed moderation request is stored in the DynamoDB table:

```text
ModerationLogs
```

The `requestId` is used as the partition key.

## Notifications

Notifications are generated when the moderation decision is:

```text
FLAGGED
```

The notification system sends alerts through:

```text
Amazon SNS
     |
     +--> Email

Discord Webhook
     |
     +--> #moderation-alerts
```

## API Gateway Configuration

| Configuration | Value |
|---|---|
| API Type | HTTP API |
| API Name | SmartContentModeration |
| Route | `POST /moderate` |
| Integration | AWS Lambda |
| Lambda Function | SmartContentModerationFunction |
| Payload Format | 2.0 |
| Stage | `$default` |
| Region | `ap-south-1` |

## Example Workflow

1. Client sends an image URL.
2. API Gateway receives the `POST /moderate` request.
3. API Gateway invokes the Lambda function.
4. Lambda downloads and validates the image.
5. Lambda sends the image to Amazon Rekognition.
6. Rekognition returns moderation labels and confidence scores.
7. The decision engine determines `APPROVED` or `FLAGGED`.
8. The result is stored in DynamoDB.
9. If flagged, SNS email and Discord notifications are generated.
10. The API returns the moderation result to the client.

