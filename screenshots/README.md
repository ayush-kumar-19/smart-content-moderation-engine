# Project Screenshots and Evidence

This directory contains screenshots demonstrating the deployment, testing, and operation of the Smart Content Moderation Engine.

## AWS Evidence

The `aws/` directory can contain screenshots of:

- Lambda function configuration
- Lambda environment variables
- IAM permissions
- API Gateway configuration
- DynamoDB table
- DynamoDB moderation records
- SNS topic and subscription
- Rekognition-related execution results
- CloudWatch Logs

## Testing Evidence

The `testing/` directory can contain screenshots of:

- Safe image test result
- Flagged image test result
- SNS email notification
- Discord moderation notification
- API Gateway response
- DynamoDB audit record
- CloudWatch execution logs

## GitHub Evidence

The `github/` directory can contain screenshots of:

- GitHub repository
- Repository structure
- README
- Lambda source code
- Documentation files
- Git commit history

## Recommended Naming Convention

Use descriptive names such as:

```text
lambda-configuration.png
iam-permissions.png
api-gateway.png
dynamodb-table.png
dynamodb-record.png
sns-email.png
discord-alert.png
cloudwatch-logs.png
safe-test.png
flagged-test.png
github-repository.png


Security

Before adding screenshots to a public GitHub repository, verify that screenshots do not expose:

AWS access keys
Secret keys
Passwords
Discord webhook URLs
Authentication tokens
Other confidential credentials
```text
