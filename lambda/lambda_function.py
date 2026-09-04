import json
import os
import uuid
import urllib.request
import urllib.parse
import urllib.error
import socket
import ipaddress
from datetime import datetime, timezone
from decimal import Decimal

import boto3


# ============================================================
# AWS CLIENTS
# ============================================================

rekognition = boto3.client("rekognition")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

TABLE_NAME = os.environ["TABLE_NAME"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]

table = dynamodb.Table(TABLE_NAME)


# ============================================================
# CONFIGURATION
# ============================================================

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # Rekognition limit: 5 MB
MIN_CONFIDENCE = 70.0

HIGH_THRESHOLD = 90.0
MEDIUM_THRESHOLD = 70.0


# ============================================================
# RESPONSE HELPER
# ============================================================

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }


# ============================================================
# URL VALIDATION
# ============================================================

def validate_url(url):
    """Validate that the image URL is HTTPS and does not
    resolve to a private/local IP address.
    """

    try:
        parsed = urllib.parse.urlparse(url)

        if parsed.scheme != "https":
            raise ValueError("Only HTTPS image URLs are allowed")

        if not parsed.hostname:
            raise ValueError("Invalid image URL")

        hostname = parsed.hostname.lower()

        blocked_hostnames = {
            "localhost",
            "localhost.localdomain",
            "metadata.google.internal"
        }

        if hostname in blocked_hostnames:
            raise ValueError("Blocked hostname")

        # Resolve hostname and reject private/local addresses.
        addresses = socket.getaddrinfo(
            hostname,
            443,
            type=socket.SOCK_STREAM
        )

        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_link_local
                or ip.is_reserved
                or ip.is_multicast
            ):
                raise ValueError("Image URL resolves to a blocked address")

        return True

    except ValueError:
        raise

    except Exception as e:
        raise ValueError(f"Could not validate image URL: {str(e)}")


# ============================================================
# DOWNLOAD IMAGE
# ============================================================

def download_image(url):
    """Download an image from a public HTTPS URL.
    Maximum supported size is 5 MB.
    """

    validate_url(url)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "SmartContentModeration/1.0"
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as result:

            content_type = result.headers.get("Content-Type", "").lower()

            # Reject obvious non-image responses.
            if (
                content_type
                and not content_type.startswith("image/")
                and "application/octet-stream" not in content_type
            ):
                raise ValueError(
                    f"URL does not appear to contain an image. "
                    f"Content-Type: {content_type}"
                )

            content_length = result.headers.get("Content-Length")

            if content_length:
                try:
                    if int(content_length) > MAX_IMAGE_SIZE:
                        raise ValueError("Image is larger than 5 MB")
                except ValueError:
                    pass

            image_bytes = result.read(MAX_IMAGE_SIZE + 1)

            if len(image_bytes) > MAX_IMAGE_SIZE:
                raise ValueError("Image is larger than 5 MB")

            if len(image_bytes) == 0:
                raise ValueError("Downloaded image is empty")

            return image_bytes

    except urllib.error.HTTPError as e:
        raise ValueError(f"Unable to download image. HTTP {e.code}")

    except urllib.error.URLError as e:
        raise ValueError(f"Unable to download image: {e.reason}")


# ============================================================
# REKOGNITION MODERATION
# ============================================================

def moderate_image(image_bytes):

    print("REKOGNITION_STARTED")

    result = rekognition.detect_moderation_labels(
        Image={
            "Bytes": image_bytes
        },
        MinConfidence=MIN_CONFIDENCE
    )

    labels = result.get("ModerationLabels", [])

    moderation_labels = []

    for label in labels:
        name = label.get("Name", "Unknown")
        confidence = float(label.get("Confidence", 0))

        moderation_labels.append({
            "name": name,
            "confidence": round(confidence, 2)
        })

    print(
        f"REKOGNITION_COMPLETED: "
        f"{len(moderation_labels)} labels detected"
    )

    return moderation_labels


# ============================================================
# DECISION
# ============================================================

def determine_verdict(labels):

    if not labels:
        return "APPROVED", "NONE", 0.0

    maximum_confidence = max(
        label["confidence"]
        for label in labels
    )

    if maximum_confidence >= HIGH_THRESHOLD:
        severity = "HIGH"

    elif maximum_confidence >= MEDIUM_THRESHOLD:
        severity = "MEDIUM"

    else:
        severity = "LOW"

    return "FLAGGED", severity, maximum_confidence


# ============================================================
# SNS NOTIFICATION
# ============================================================

def send_sns_notification(
    request_id,
    image_url,
    labels,
    severity,
    confidence
):

    label_text = ", ".join(
        f"{label['name']} ({label['confidence']:.2f}%)"
        for label in labels
    )

    message = f"""
Smart Content Moderation Alert

Request ID: {request_id}

Verdict: FLAGGED
Severity: {severity}
Maximum Confidence: {confidence:.2f}%

Detected Labels:
{label_text}

Image URL:
{image_url}

Action Required:
Please review this content.
""".strip()

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="Content Moderation Alert",
        Message=message
    )

    print("SNS_NOTIFICATION_SENT")


# ============================================================
# DISCORD NOTIFICATION
# ============================================================

def send_discord_notification(
    request_id,
    image_url,
    labels,
    severity,
    confidence
):

    label_text = "\n".join(
        f"• {label['name']} — {label['confidence']:.2f}%"
        for label in labels
    )

    discord_message = {
        "content": (
            "🚨 **Content Moderation Alert**\n\n"
            f"**Request ID:** `{request_id}`\n"
            f"**Verdict:** `FLAGGED`\n"
            f"**Severity:** `{severity}`\n"
            f"**Maximum Confidence:** `{confidence:.2f}%`\n\n"
            f"**Detected Labels:**\n{label_text}\n\n"
            f"**Image:** {image_url}"
        )
    }

    data = json.dumps(discord_message).encode("utf-8")

    request = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "SmartContentModeration/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as result:
            if result.status in (200, 204):
                print("DISCORD_NOTIFICATION_SENT")
            else:
                raise ValueError(
                    f"Discord returned HTTP {result.status}"
                )

    except urllib.error.HTTPError as e:
        raise ValueError(
            f"Discord notification failed. HTTP {e.code}"
        )


# ============================================================
# DYNAMODB AUDIT LOG
# ============================================================

def save_audit_log(
    request_id,
    image_url,
    verdict,
    severity,
    labels,
    confidence,
    notification_status
):

    item = {
        "requestId": request_id,
        "imageUrl": image_url,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "verdict": verdict,
        "severity": severity,

        "labels": [
            label["name"]
            for label in labels
        ],

        "confidence": Decimal(
            str(round(confidence, 2))
        ),

        "notificationStatus": notification_status
    }

    table.put_item(Item=item)

    print("DYNAMODB_WRITE_COMPLETED")


# ============================================================
# MAIN LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    request_id = str(uuid.uuid4())

    print(f"REQUEST_RECEIVED: {request_id}")

    try:

        # ----------------------------------------------------
        # Parse request body
        # ----------------------------------------------------

        body = event.get("body")

        if body is not None:

            if isinstance(body, str):

                try:
                    body = json.loads(body)

                except json.JSONDecodeError:
                    return response(
                        400,
                        {
                            "error": "Invalid JSON request body",
                            "requestId": request_id
                        }
                    )

        else:
            body = event

        if not isinstance(body, dict):

            return response(
                400,
                {
                    "error": "Request body must be a JSON object",
                    "requestId": request_id
                }
            )

        image_url = body.get("imageUrl")

        if not image_url:

            return response(
                400,
                {
                    "error": "imageUrl is required",
                    "requestId": request_id
                }
            )

        if not isinstance(image_url, str):

            return response(
                400,
                {
                    "error": "imageUrl must be a string",
                    "requestId": request_id
                }
            )

        # ----------------------------------------------------
        # Download image
        # ----------------------------------------------------

        print("IMAGE_DOWNLOAD_STARTED")

        image_bytes = download_image(image_url)

        print(
            f"IMAGE_DOWNLOAD_COMPLETED: "
            f"{len(image_bytes)} bytes"
        )

        # ----------------------------------------------------
        # Rekognition
        # ----------------------------------------------------

        labels = moderate_image(image_bytes)

        # ----------------------------------------------------
        # Decision
        # ----------------------------------------------------

        verdict, severity, confidence = determine_verdict(
            labels
        )

        print(
            f"MODERATION_RESULT: "
            f"verdict={verdict}, "
            f"severity={severity}, "
            f"confidence={confidence}"
        )

        # ----------------------------------------------------
        # Notifications
        # ----------------------------------------------------

        notification_status = "NOT_REQUIRED"

        if verdict == "FLAGGED":

            notification_results = []

            # SNS
            try:

                send_sns_notification(
                    request_id,
                    image_url,
                    labels,
                    severity,
                    confidence
                )

                notification_results.append("SNS_SENT")

            except Exception as e:

                print(
                    f"SNS_NOTIFICATION_FAILED: {str(e)}"
                )

                notification_results.append("SNS_FAILED")

            # Discord
            try:

                send_discord_notification(
                    request_id,
                    image_url,
                    labels,
                    severity,
                    confidence
                )

                notification_results.append("DISCORD_SENT")

            except Exception as e:

                print(
                    f"DISCORD_NOTIFICATION_FAILED: {str(e)}"
                )

                notification_results.append("DISCORD_FAILED")

            notification_status = ",".join(
                notification_results
            )

        # ----------------------------------------------------
        # Save audit log
        # ----------------------------------------------------

        save_audit_log(
            request_id,
            image_url,
            verdict,
            severity,
            labels,
            confidence,
            notification_status
        )

        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        if verdict == "APPROVED":

            result = {
                "requestId": request_id,
                "verdict": "APPROVED",
                "labels": [],
                "message": "No policy violations detected"
            }

        else:

            result = {
                "requestId": request_id,
                "verdict": "FLAGGED",
                "severity": severity,
                "labels": labels,
                "message": "Potentially unsafe content detected"
            }

        print(
            f"REQUEST_COMPLETED: {request_id}"
        )

        return response(200, result)

    except ValueError as e:

        print(
            f"VALIDATION_ERROR: {str(e)}"
        )

        return response(
            400,
            {
                "requestId": request_id,
                "error": str(e)
            }
        )

    except Exception as e:

        print(
            f"UNEXPECTED_ERROR: {str(e)}"
        )

        return response(
            500,
            {
                "requestId": request_id,
                "error": "Internal server error"
            }
        )