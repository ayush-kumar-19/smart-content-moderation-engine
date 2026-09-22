# API Documentation

## Smart Content Moderation Engine

The API is exposed through Amazon API Gateway and supports both image URLs and direct Base64 image uploads.

## Endpoint

```text
POST /moderate
```

## Request Format

The request must contain either `imageUrl` or `imageBase64`. The two input methods should not be supplied together.

### Option 1 — Image URL

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### Option 2 — Base64 Image Upload

```json
{
  "imageBase64": "<base64-encoded-image>",
  "fileName": "image.jpg",
  "contentType": "image/jpeg"
}
```

The frontend uses the Base64 format when a user selects an image from their laptop.

## Processing Flow

```text
Client
  ↓
API Gateway
  ↓
AWS Lambda
  ↓
Request Validation
  ↓
Amazon Rekognition
  ↓
Decision Engine
  ↓
DynamoDB
  ↓
SNS / Discord
  ↓
API Response
```

## Successful Response

Example approved response:

```json
{
  "requestId": "example-request-id",
  "verdict": "APPROVED",
  "severity": "LOW",
  "labels": [],
  "alert": false
}
```

Example flagged response:

```json
{
  "requestId": "example-request-id",
  "verdict": "FLAGGED",
  "severity": "HIGH",
  "labels": [
    {
      "name": "Violence",
      "confidence": 99.95
    }
  ],
  "alert": true
}
```

Exact labels and confidence values depend on the submitted image.

## Input Validation

The Lambda function validates:

- Required image input
- Supported input type
- Base64 validity
- Maximum Base64 upload size
- Required fields

Requests without valid image input are rejected.

## Error Handling

Typical invalid requests:

### Missing image

```json
{}
```

### Both inputs supplied

```json
{
  "imageUrl": "https://example.com/image.jpg",
  "imageBase64": "..."
}
```

### Invalid Base64

```json
{
  "imageBase64": "invalid-data"
}
```

## AWS Services

| Service | API Role |
|---|---|
| API Gateway | HTTP endpoint |
| Lambda | Request processing |
| Rekognition | Image moderation |
| DynamoDB | Audit logging |
| SNS | Email notification |
| CloudWatch | Logs and monitoring |

## Security

AWS credentials are never exposed to the frontend.

The Discord webhook is configured through:

```text
DISCORD_WEBHOOK_URL
```

and is not hardcoded into the source code.
