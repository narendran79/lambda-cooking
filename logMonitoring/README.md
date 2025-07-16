# AWS Log Monitoring System

A serverless log monitoring solution using AWS Lambda, S3, SQS, and SNS to automatically scan log files for errors and send email alerts.

## Architecture

```
Log Files → S3 Bucket → SQS Queue → Lambda Function → SNS Alert + Backup Storage
```

## Features

- **Automated Log Processing**: Processes log files uploaded to S3
- **Error Detection**: Scans for keywords: `ERROR`, `Timeout`, `Not Found`, `500`, `404`
- **Email Alerts**: Sends notifications via SNS when errors are detected
- **Backup Storage**: Archives processed logs to a separate S3 bucket
- **Free Tier Friendly**: Uses only AWS free-tier services

## Prerequisites

- AWS Account with appropriate permissions
- Python 3.9+ runtime
- AWS CLI configured (optional)

## AWS Services Used

- **S3**: Log storage and backup
- **SQS**: Message queue for event processing
- **Lambda**: Serverless function for log processing
- **SNS**: Email notifications
- **IAM**: Permissions management

## Setup Instructions

### 1. Create S3 Buckets
```bash
aws s3 mb s3://incoming-logs-dev
aws s3 mb s3://backup-for-logs-dev
```

### 2. Create SQS Queue
- Queue Name: `log-processing-queue`
- Type: Standard Queue

### 3. Configure S3 Event Notification
- Source Bucket: `incoming-logs-dev`
- Event Type: `All object create events`
- Destination: SQS Queue

### 4. Create SNS Topic
- Topic Name: `logAlert`
- Subscribe your email address

### 5. Deploy Lambda Function
- Runtime: Python 3.9+
- Handler: `logmonitoring.lambda_handler`
- Trigger: SQS Queue

### 6. Set IAM Permissions
Lambda execution role needs:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::incoming-logs-dev/*",
                "arn:aws:s3:::backup-for-logs-dev/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "arn:aws:sns:us-east-1:*:logAlert"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sqs:ReceiveMessage",
                "sqs:DeleteMessage",
                "sqs:GetQueueAttributes"
            ],
            "Resource": "arn:aws:sqs:us-east-1:*:log-processing-queue"
        }
    ]
}
```

## Configuration

Update these variables in `logmonitoring.py`:

```python
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:YOUR_ACCOUNT:logAlert'
SOURCE_BUCKET = 'incoming-logs-dev'
BACKUP_BUCKET = 'backup-for-logs-dev'
ALERT_KEYWORDS = ['ERROR', 'Timeout', 'Not Found', '500', '404']
```

## Usage

1. Upload log files to `incoming-logs-dev` bucket
2. Lambda automatically processes the files
3. If errors are found, you'll receive an email alert
4. Processed logs are backed up to `backup-for-logs-dev`

## Testing

### Test Event (SQS Format)
```json
{
  "Records": [
    {
      "messageId": "test-message-id",
      "receiptHandle": "test-receipt-handle",
      "body": "{\"Records\":[{\"eventVersion\":\"2.1\",\"eventSource\":\"aws:s3\",\"eventName\":\"ObjectCreated:Put\",\"s3\":{\"bucket\":{\"name\":\"incoming-logs-dev\"},\"object\":{\"key\":\"test-log.txt\"}}}]}",
      "attributes": {
        "ApproximateReceiveCount": "1"
      }
    }
  ]
}
```

### Sample Log File
```
2024-01-15 10:30:00 INFO Application started successfully
2024-01-15 10:31:00 ERROR Database connection failed
2024-01-15 10:32:00 INFO Retrying connection
2024-01-15 10:33:00 Timeout occurred while connecting to service
```

## Monitoring

- Check CloudWatch Logs for Lambda execution details
- Monitor SQS queue for message processing
- Verify email delivery through SNS

## Cost Optimization

This solution is designed for AWS Free Tier:
- Lambda: 1M free requests/month
- S3: 5GB free storage
- SQS: 1M free requests/month
- SNS: 1,000 free email notifications/month

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**: Check IAM permissions
2. **No Email Alerts**: Verify SNS topic subscription
3. **SQS Messages Not Processing**: Check Lambda trigger configuration
4. **Files Not Found**: Ensure test files exist in S3

### Debug Steps

1. Check CloudWatch Logs for detailed error messages
2. Verify S3 event notifications are configured
3. Test SNS topic manually
4. Validate IAM role permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please create an issue in the repository or contact the DevOps team.