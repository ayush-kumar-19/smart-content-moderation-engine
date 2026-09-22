# System Architecture

## Smart Content Moderation Engine

The Smart Content Moderation Engine is a serverless AWS application that automatically analyzes images and generates moderation decisions.

---

## High-Level Architecture

```text
                         USER
                          |
                          v
                 +----------------+
                 | S3 Frontend    |
                 | Web Dashboard   |
                 +----------------+
                    /          \
                   /            \
          Image URL          Laptop Upload
                   \            /
                    \          /
                     v        v
                 +----------------+
                 | API Gateway    |
                 | POST /moderate |
                 +----------------+
                         |
                         v
                 +----------------+
                 | AWS Lambda     |
                 | Moderation     |
                 +----------------+
                         |
                         v
                 +----------------+
                 | Rekognition    |
                 | Image Analysis |
                 +----------------+
                         |
                         v
                 +----------------+
                 | Decision Engine|
                 +----------------+
                    /           \
                   /             \
                  v               v
        +----------------+   +-------------------+
        | DynamoDB       |   | Notifications      |
        | ModerationLogs |   | SNS + Discord      |
        +----------------+   +-------------------+
                                    |
                                    v
                                  Email
```

---

## 1. Frontend Layer

The frontend is a static web application hosted on Amazon S3.

Files:

```text
frontend/
├── index.html
├── style.css
└── script.js
```

The dashboard provides:

- Image URL submission
- Laptop image upload
- Moderation result display
- Detection information
- Severity information
- Alert status

---

## 2. API Gateway Layer

Amazon API Gateway provides the HTTP interface.

Route:

```text
POST /moderate
```

It receives the frontend request and invokes the Lambda function.

---

## 3. Lambda Layer

AWS Lambda contains the main moderation logic.

Responsibilities:

1. Validate request input.
2. Accept image URL or Base64 image.
3. Decode Base64 data when necessary.
4. Submit the image to Rekognition.
5. Evaluate moderation labels.
6. Generate the moderation decision.
7. Store the result.
8. Trigger notifications when required.
9. Return the result to the frontend.

---

## 4. Amazon Rekognition

Amazon Rekognition performs image moderation using:

```text
DetectModerationLabels
```

The service returns moderation labels and confidence values.

Examples of detected categories can include:

```text
Violence
Weapons
Explicit Content
```

The actual labels depend on the submitted image.

---

## 5. Decision Engine

The decision engine evaluates Rekognition results.

```text
Image
 ↓
Rekognition Labels
 ↓
Confidence Evaluation
 ↓
Moderation Rules
 ↓
APPROVED / FLAGGED
```

Flagged content can additionally receive a severity classification.

---

## 6. DynamoDB

The `ModerationLogs` table stores moderation audit information.

Partition key:

```text
requestId
```

The stored information can include:

- Request ID
- Image reference
- Verdict
- Severity
- Detected labels
- Confidence values
- Timestamp
- Alert information

---

## 7. Notification Layer

### SNS

```text
Lambda → SNS → Email
```

### Discord

```text
Lambda → Discord Webhook → Moderation Channel
```

The Discord webhook is stored as a Lambda environment variable.

---

## 8. CloudWatch

Amazon CloudWatch Logs records Lambda execution information for debugging, monitoring, and error investigation.

---

## 9. IAM

AWS IAM controls permissions for the Lambda execution role.

Role:

```text
SmartContentModerationLambdaRole
```

---

## 10. Data Flow

### Image URL

```text
User
 ↓
Frontend
 ↓
API Gateway
 ↓
Lambda
 ↓
Rekognition
 ↓
Decision Engine
 ↓
DynamoDB
 ↓
Response
```

### Laptop Upload

```text
User
 ↓
Frontend
 ↓
Base64 Encoding
 ↓
API Gateway
 ↓
Lambda
 ↓
Base64 Decoding
 ↓
Rekognition
 ↓
Decision Engine
 ↓
DynamoDB
 ↓
SNS / Discord if flagged
 ↓
Frontend
```

---

## 11. Security Considerations

- AWS credentials are not exposed in the frontend.
- Lambda uses an IAM execution role.
- Discord webhook configuration is stored in Lambda environment variables.
- Sensitive credentials are excluded from GitHub.
- The repository contains only a reusable S3 bucket policy example.

---

## 12. Future Production Architecture

For a production deployment:

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
 ↓
Lambda
```

This provides HTTPS delivery and stronger S3 access control.
