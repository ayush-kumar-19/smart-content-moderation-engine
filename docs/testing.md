# Testing Documentation

The system was tested across the backend, AWS services, API, notifications, and frontend.

---

## Test 1 — Safe Image

### Objective

Verify that an image without detected moderation violations is approved.

### Expected Result

```text
Verdict: APPROVED
Alert: False
```

### Result

The safe image was successfully processed and classified as approved.

```text
Status: PASS
```

---

## Test 2 — Flagged Image

### Objective

Verify that an image containing moderation violations is flagged.

### Expected Result

```text
Verdict: FLAGGED
Severity: HIGH
Alert: True
```

### Result

The flagged image was detected by Amazon Rekognition with labels including:

```text
Weapons
Violence
```

The moderation engine generated a high-severity flagged result.

```text
Status: PASS
```

---

## Test 3 — DynamoDB Logging

The moderation result was successfully stored in:

```text
ModerationLogs
```

```text
Status: PASS
```

---

## Test 4 — SNS Notification

A flagged-content notification was successfully received through the configured email subscription.

```text
Status: PASS
```

---

## Test 5 — Discord Notification

The moderation alert was successfully delivered to the configured Discord channel.

```text
Status: PASS
```

---

## Test 6 — CloudWatch Logging

Lambda execution information was successfully recorded in Amazon CloudWatch Logs.

```text
Status: PASS
```

---

## Test 7 — API Gateway

The API Gateway moderation endpoint successfully processed a safe image request.

```text
Status: PASS
```

---

## Test 8 — Frontend Image URL

The dashboard successfully sent an image URL to the moderation API and displayed the returned moderation result.

```text
Status: PASS
```

---

## Test 9 — Frontend Laptop Upload

### Objective

Verify that users can select an image directly from their laptop.

### Process

```text
Laptop Image
     ↓
Browser File Input
     ↓
Base64 Conversion
     ↓
API Gateway
     ↓
Lambda
     ↓
Amazon Rekognition
```

### Result

The uploaded image was successfully accepted by the dashboard and processed through the moderation pipeline.

```text
Status: PASS
```

---

## Overall Testing Result

| Component | Result |
|---|---|
| Lambda | PASS |
| Rekognition | PASS |
| DynamoDB | PASS |
| SNS | PASS |
| Discord | PASS |
| CloudWatch | PASS |
| API Gateway | PASS |
| Frontend URL moderation | PASS |
| Frontend laptop upload | PASS |

The end-to-end moderation workflow was successfully validated.
