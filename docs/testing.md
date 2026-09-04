# Testing Documentation

## Smart Content Moderation Engine

This document records the testing performed on the Smart Content Moderation Engine and the expected results.

## Testing Objectives

The system was tested to verify that:

- Valid image URLs are processed correctly.
- Safe images are approved.
- Unsafe images are flagged.
- Severity is calculated correctly.
- Moderation results are stored in DynamoDB.
- Flagged content generates SNS email notifications.
- Flagged content generates Discord notifications.
- Lambda execution is recorded in CloudWatch.
- API Gateway correctly invokes Lambda.

## Test Environment

| Component | Configuration |
|---|---|
| AWS Region | `ap-south-1` |
| Lambda | `SmartContentModerationFunction` |
| API | `SmartContentModeration` |
| Route | `POST /moderate` |
| DynamoDB | `ModerationLogs` |
| SNS Topic | `content-moderation-alerts` |
| Runtime | Python 3.14 |

## Test Case 1: Safe Image

### Objective

Verify that an image containing normal, safe content is approved.

### Expected Result

```text
Decision: APPROVED
Severity: LOW
Labels: []
```

### Actual Result

```text
Decision: APPROVED
No moderation labels detected.
DynamoDB audit record created.
```

### Status

```text
PASS
```

## Test Case 2: Flagged Image

### Objective

Verify that an image containing unsafe content is detected and flagged.

### Expected Result

```text
Decision: FLAGGED
Severity: HIGH
```

### Actual Result

Amazon Rekognition detected moderation labels including:

```text
Weapons
Violence
```

The highest confidence was approximately:

```text
99.95%
```

The system classified the content as:

```text
FLAGGED
HIGH
```

### Status

```text
PASS
```

## Test Case 3: DynamoDB Audit Logging

### Objective

Verify that moderation requests are stored in DynamoDB.

### Expected Result

A record should be created in:

```text
ModerationLogs
```

using:

```text
requestId
```

as the partition key.

### Actual Result

Moderation records were successfully stored and verified in DynamoDB.

### Status

```text
PASS
```

## Test Case 4: SNS Email Notification

### Objective

Verify that flagged content generates an email notification.

### Expected Result

A notification should be published to:

```text
content-moderation-alerts
```

and delivered to the confirmed email subscription.

### Actual Result

The flagged-image test generated an SNS notification and the email was successfully received.

### Status

```text
PASS
```

## Test Case 5: Discord Notification

### Objective

Verify that flagged content generates a Discord alert.

### Expected Result

A notification should appear in:

```text
#moderation-alerts
```

### Actual Result

The Discord moderation channel successfully received the flagged-content notification.

### Status

```text
PASS
```

## Test Case 6: CloudWatch Logging

### Objective

Verify that Lambda execution information is available for monitoring and troubleshooting.

### Expected Result

Lambda execution logs should be available in Amazon CloudWatch Logs.

### Actual Result

CloudWatch logs were verified for Lambda executions, moderation results, and processing activity.

### Status

```text
PASS
```

## Test Case 7: API Gateway Integration

### Objective

Verify that API Gateway successfully invokes the Lambda function.

### Request

```http
POST /moderate
Content-Type: application/json
```

Example body:

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### Expected Result

API Gateway should invoke Lambda and return the moderation result.

### Actual Result

The deployed API successfully processed a safe public image and returned an:

```text
APPROVED
```

moderation response.

### Status

```text
PASS
```

## Test Summary

| Test Case | Expected Result | Status |
|---|---|---|
| Safe image | APPROVED | PASS |
| Unsafe image | FLAGGED | PASS |
| Severity calculation | Correct severity | PASS |
| DynamoDB logging | Record stored | PASS |
| SNS notification | Email received | PASS |
| Discord notification | Alert received | PASS |
| CloudWatch logging | Logs available | PASS |
| API Gateway integration | API returns result | PASS |

## Moderation Decision Testing

The decision engine follows:

```text
No labels
    |
    v
APPROVED
```

For detected moderation labels:

```text
Confidence >= 90%
        |
        v
FLAGGED + HIGH
```

```text
Confidence 70% - 89.99%
        |
        v
FLAGGED + MEDIUM
```

## End-to-End Test Flow

```text
Client
  |
  v
API Gateway
  |
  v
Lambda
  |
  v
Rekognition
  |
  v
Decision Engine
  |
  +-----------> DynamoDB
  |
  +-- FLAGGED -> SNS -> Email
  |
  +-- FLAGGED -> Discord
  |
  v
API Response
```

## Testing Conclusion

The core Smart Content Moderation Engine workflow was successfully tested.

The system successfully:

- Processes image URLs.
- Detects unsafe content using Amazon Rekognition.
- Approves safe content.
- Flags unsafe content.
- Calculates moderation severity.
- Stores moderation results in DynamoDB.
- Sends email alerts through SNS.
- Sends Discord alerts.
- Produces CloudWatch logs.
- Exposes the moderation functionality through API Gateway.

