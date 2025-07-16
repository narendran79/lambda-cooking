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
## Usage

1. Upload log files to `incoming-logs-dev` bucket
2. Lambda automatically processes the files
3. If errors are found, you'll receive an email alert
4. Processed logs are backed up to `backup-for-logs-dev`

### Sample Log File
```
2024-01-15 10:30:00 INFO Application started successfully
2024-01-15 10:31:00 ERROR Database connection failed
2024-01-15 10:32:00 INFO Retrying connection
2024-01-15 10:33:00 Timeout occurred while connecting to service
```

## Monitoring
- Monitor SQS queue for message processing
- Verify email delivery through SNS


## Troubleshooting

### Common Issues

1. **403 Forbidden Error**: Check IAM permissions
2. **No Email Alerts**: Verify SNS topic subscription
3. **SQS Messages Not Processing**: Check Lambda trigger configuration
4. **Files Not Found**: Ensure test files exist in S3
