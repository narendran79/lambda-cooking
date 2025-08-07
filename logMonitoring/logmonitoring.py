import boto3
import json
from datetime import datetime

# Initialize AWS clients for S3 and SNS
s3_client = boto3.client('s3')
sns_client = boto3.client('sns')

# SNS topic ARN for sending alerts
SNS_TOPIC_ARN = '<your-sns-arn>'

# Keywords to look for in the logs that indicate potential issues
ALERT_KEYWORDS = ['ERROR', 'Timeout', 'Not Found', '500', '404']

# Source bucket where logs are initially stored
SOURCE_BUCKET = 'incoming-logs-dev'

# Backup bucket to store processed logs
BACKUP_BUCKET = 'backup-for-logs-dev'

def alert_email(error_details, filename):
    """
    Sends an alert email via SNS with tabular format showing error breakdown.
    """
    # Create table header
    table = "\n" + "="*60 + "\n"
    table += f"{'KEYWORD':<15} | {'COUNT':<10} | {'PERCENTAGE':<10}\n"
    table += "-"*60 + "\n"
    
    total_errors = sum(error_details.values())
    
    # Add table rows
    for keyword, count in error_details.items():
        if count > 0:
            percentage = round((count/total_errors)*100, 1)
            table += f"{keyword:<15} | {count:<10} | {percentage}%\n"
    
    table += "="*60 + "\n"
    table += f"{'TOTAL ERRORS':<15} | {total_errors:<10} | 100.0%\n"
    table += "="*60
    
    email_message = f'''🚨 LOG ALERT NOTIFICATION 🚨

File: {filename}
Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Total Error Count: {total_errors}

ERROR BREAKDOWN:{table}

Please investigate and resolve these issues immediately.

Regards,
DevOps Team'''
    
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
    error_details = {}
    
    # Count occurrences of each keyword
    for keyword in ALERT_KEYWORDS:
        count = payload.count(keyword)
        error_details[keyword] = count
    
    total_errors = sum(error_details.values())
    
    if total_errors > 0:
        alert_email(error_details, filename)
        print(f"Alert triggered: {total_errors} error keywords found in logs")

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
