# Smart Content Moderation Engine

An AWS serverless content moderation system that uses **Amazon Rekognition** to analyze images, automatically classify potentially unsafe content, store moderation results, and send real-time alerts.

The project includes a web dashboard hosted on **Amazon S3** that supports both image URLs and direct laptop image uploads.

---

## 🚀 Project Overview

The Smart Content Moderation Engine provides an automated pipeline for detecting potentially inappropriate or unsafe images.

### Core workflow

```text
                    S3 Frontend
                   Web Dashboard
                  /            \
                 /              \
          Image URL          Laptop Upload
                 \              /
                  \            /
                   API Gateway
                       ↓
                    Lambda
                       ↓
             Amazon Rekognition
                       ↓
                Decision Engine
                  /         \
                 /           \
          DynamoDB        Notifications
                         /           \
                       SNS         Discord
                        ↓
                      Email
```

---

## ✨ Key Features

- AI-powered image moderation using Amazon Rekognition
- Image URL moderation
- Direct image upload from laptop
- Base64 image processing through Lambda
- Automatic APPROVED / FLAGGED decision
- Detection of moderation labels such as violence and weapons
- Confidence-based severity classification
- DynamoDB audit logging
- Amazon SNS email alerts
- Discord moderation alerts
- CloudWatch logging
- REST API through Amazon API Gateway
- Serverless AWS architecture
- Static frontend hosted on Amazon S3
- Responsive moderation dashboard

---

## 🏗️ AWS Architecture

| Service | Purpose |
|---|---|
| Amazon API Gateway | Receives moderation requests |
| AWS Lambda | Executes moderation logic |
| Amazon Rekognition | Detects unsafe image content |
| Amazon DynamoDB | Stores moderation audit records |
| Amazon SNS | Sends email notifications |
| Amazon S3 | Hosts the frontend dashboard |
| Amazon CloudWatch | Stores Lambda execution logs |
| IAM | Controls AWS resource permissions |

---

## 📂 Project Structure

```text
smart-content-moderation-engine/
│
├── README.md
├── LICENSE
├── .gitignore
├── bucket-policy.example.json
│
├── lambda/
│   └── lambda_function.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│
├── api/
│
├── architecture/
│   └── architecture.md
│
├── docs/
│   ├── api.md
│   ├── setup.md
│   ├── deployment.md
│   └── testing.md
│
└── screenshots/
    ├── README.md
    ├── aws/
    ├── testing/
    └── github/
```

---

## 🖥️ Frontend Dashboard

The frontend is a static web application hosted using Amazon S3 Static Website Hosting.

The dashboard supports two input methods:

### 1. Image URL

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### 2. Laptop Image Upload

Users can select an image directly from their laptop.

```text
Laptop Image
     ↓
Read File
     ↓
Convert to Base64
     ↓
API Gateway
     ↓
Lambda
     ↓
Amazon Rekognition
```

The uploaded image is not stored permanently by the moderation API. It is decoded in Lambda and passed to Amazon Rekognition for analysis.

---

## 🔌 API

### Endpoint

```text
POST /moderate
```

### Image URL Request

```json
{
  "imageUrl": "https://example.com/image.jpg"
}
```

### Base64 Upload Request

```json
{
  "imageBase64": "<base64-encoded-image>",
  "fileName": "image.jpg",
  "contentType": "image/jpeg"
}
```

The API accepts either `imageUrl` or `imageBase64`.

---

## 🧠 Moderation Process

1. Receive the image through API Gateway.
2. AWS Lambda validates the request.
3. If an image URL is supplied, Lambda uses the URL.
4. If a Base64 image is supplied, Lambda decodes it.
5. Lambda sends the image to Amazon Rekognition.
6. Rekognition returns moderation labels and confidence scores.
7. The decision engine evaluates the detected labels.
8. The image is classified as `APPROVED` or `FLAGGED`.
9. The moderation result is stored in DynamoDB.
10. High-risk content triggers notifications through SNS and Discord.
11. The API returns the moderation result to the frontend.

---

## 🗄️ DynamoDB Audit Logging

Moderation requests are stored in the `ModerationLogs` DynamoDB table.

The audit record contains information such as:

- Request ID
- Image reference
- Moderation verdict
- Detected labels
- Confidence scores
- Severity
- Timestamp
- Processing information

---

## 🔔 Notifications

### Amazon SNS

SNS sends email notifications when content is flagged.

### Discord

The Lambda function can send moderation alerts to a configured Discord webhook.

The Discord webhook URL is stored as a Lambda environment variable and is not hardcoded in the source code.

---

## 🧪 Testing

The following components were tested successfully:

- Lambda safe-content test
- Lambda flagged-content test
- Amazon Rekognition integration
- DynamoDB logging
- SNS email notification
- Discord notification
- CloudWatch logging
- API Gateway integration
- Frontend image URL moderation
- Frontend laptop image upload

Example:

```text
SAFE IMAGE
Status: APPROVED
Alert: False
```

```text
FLAGGED IMAGE
Status: FLAGGED
Severity: HIGH
Detected Labels: Weapons, Violence
Alert: True
```

---

## 🔐 Security Notes

- AWS permissions are controlled using IAM.
- Discord webhook configuration is stored using Lambda environment variables.
- Secrets and credentials are not committed to GitHub.
- `.gitignore` prevents sensitive local configuration from being committed.
- `bucket-policy.example.json` contains a placeholder bucket name.

The current frontend uses an S3 static website endpoint over HTTP.

For a production deployment, the frontend can be placed behind **Amazon CloudFront with HTTPS**, preferably using a private S3 bucket and CloudFront Origin Access Control.

---

## 🔮 Future Enhancements

- Amazon S3 storage for uploaded images
- Amazon CloudFront + HTTPS for frontend delivery
- Authentication and role-based access
- Admin moderation history dashboard
- More advanced moderation rules
- Additional notification channels
- Batch image moderation
- Video moderation
- Machine-learning-based anomaly detection
- CloudWatch dashboards and alarms
- Infrastructure as Code using AWS CDK or Terraform

---

## 📚 Documentation

- `docs/api.md` — API specification
- `docs/setup.md` — AWS setup
- `docs/deployment.md` — Deployment process
- `docs/testing.md` — Testing and validation
- `architecture/architecture.md` — System architecture

---

## 📜 License

This project is developed for academic and educational purposes.

See `LICENSE` for details.
