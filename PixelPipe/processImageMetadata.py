import json
import boto3
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

DYNAMODB_TABLE = "image-metadata-table"
SNS_TOPIC_NAME = "image-metadata-topic"

def lambda_handler(event, context):
    try:
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        response = s3.head_object(Bucket=bucket, Key=key)
        metadata = {
            'image_name': key,
            'bucket_name': bucket,
            'image_size': response['ContentLength'],
            'last_modified': response['LastModified'].isoformat(),
            'content_type': response['ContentType'],
            'processed_at': datetime.now().isoformat()
        }

        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(Item=metadata)

        topic_arn = None
        topics = sns.list_topics()['Topics']
        for topic in topics:
            if SNS_TOPIC_NAME in topic['TopicArn']:
                topic_arn = topic['TopicArn']
                print(topic_arn)
                break
            else:
                print("Topic not found")
        
        if topic_arn:
            message = f"New image uploaded: {key}"
            sns.publish(TopicArn=topic_arn, Message=message, Subject="Image Upload Notification")
            print("Notification sent successfully")

        return {
            'statusCode': 200,
            'body': json.dumps('Metadata processed successfully')
        }
    except Exception as e:
        print(f"Error processing metadata: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing metadata')
        }
