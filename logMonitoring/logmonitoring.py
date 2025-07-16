import boto3
import json
from datetime import datetime

# Initialize AWS clients for S3 and SNS
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# SNS topic ARN for sending alerts
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:039612876144:logAlert'

# Keywords to look for in the logs that indicate potential issues
ALERT_KEYWORDS = ['ERROR', 'Timeout', 'Not Found', '500', '404']

# Source bucket where logs are initially stored
SOURCE_BUCKET = 'incoming-logs-dev'

# Backup bucket to store processed logs
BACKUP_BUCKET = 'backup-for-logs-dev'

def alert_email(count, filename):
    """
    Sends an alert email via SNS if error keywords are found in the logs.
    """
    email_message = f'''Alert From Logs !!!

This email is to inform you that we have received some error logs. Please check and resolve the issue.
File: {filename}
Count of keywords are appeared in the logs: {count}

Keywords can be ERROR, Timeout, Not Found, 500, 404
Regards,
DevOps Team
'''
    response = sns_client.publish(TopicArn=SNS_TOPIC_ARN, Message=email_message)
    print("Alert sent for error logs")
    return response

def store_logs(payload):
    """
    Stores the log content in the backup S3 bucket with a timestamped filename.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    key = f'logs/service_logs_{timestamp}.txt'
    s3_client.put_object(Bucket=BACKUP_BUCKET, Key=key, Body=payload)
    print("Logs stored in S3 bucket successfully.")

def scan_payload(payload, filename):
    """
    Scans the log content for alert keywords and triggers an alert if any are found.
    """
    count = sum(1 for word in ALERT_KEYWORDS if word in payload)
    if count > 0:
        alert_email(count, filename)
        print("Alert triggered due to error keywords in logs")

def lambda_handler(event, context):
    """
    AWS Lambda handler function to process incoming S3 event notifications.
    It reads the log file, scans for errors, and stores the logs in a backup bucket.
    """
    try:
        for records in event['Records']:
            # Parse the SQS message body to extract S3 event details
            s3_event = json.loads(records['body'])

            for s3_record in s3_event['Records']:
                # Extract bucket name and object key from the event
                bucket_name = s3_record['s3']['bucket']['name']
                object_key = s3_record['s3']['object']['key']

                # Retrieve the log file from S3
                response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                log_content = response['Body'].read().decode('utf-8')

                # Scan the log content for alert keywords
                scan_payload(log_content, object_key)

                # Store the log content in the backup bucket
                store_logs(log_content)

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully completed')
        }
    except Exception as e:
        # Handle any errors that occur during processing
        print(f"Error processing logs: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing logs')
        }
