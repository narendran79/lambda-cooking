import boto3

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
sns = boto3.client('sns')

TOPIC_ARN = <your-sns-topic-arn>
OBJECT_COUNT_LIMIT = 5

def count_object(buckets):
    for bucket in buckets:
        bucket_name = bucket['Name']
        bucket_resource = s3_resource.Bucket(bucket_name)
        object_count = 0
        for obj in bucket_resource.objects.all():
            object_count += 1
        print(f"Bucket: {bucket_name}, Object Count: {object_count}")

        if object_count > OBJECT_COUNT_LIMIT:
            alert_size(bucket_name)
            print(f"The object size exceeds the limit")

def alert_size(bucket_name):
    email_message = f'''Alert From S3 !!!

This email is to inform you that the bucket "{bucket_name}" has exceeded the object count limit of {OBJECT_COUNT_LIMIT}.
Please delete unused objects from this bucket.

Regards,
DevOps Team
'''
    response = sns.publish(TopicArn=TOPIC_ARN, Message=email_message)
    print(f"Alert sent for object count on bucket: {bucket_name}")
    return response

def versioning_check(buckets):
    for bucket in buckets:
        bucket_name = bucket['Name']
        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
        
        if versioning.get('Status', 'Disabled') != 'Enabled':
            print(f"Versioning is not enabled on: {bucket_name}")
            alert_versioning(bucket_name)

def alert_versioning(bucket_name):
    email_message = f'''Alert From S3 !!!

This email is to inform you that versioning is currently DISABLED on the bucket "{bucket_name}".
Please check the bucket configuration and re-enable versioning to keep a track.

Regards,
DevOps Team
'''
    response = sns.publish(TopicArn=TOPIC_ARN, Message=email_message)
    print(f"Alert sent for versioning on bucket: {bucket_name}")
    return response

def lambda_handler(event, context):
    response = s3_client.list_buckets()
    buckets = response.get('Buckets', [])

    if not buckets:
        print("No buckets found.")
        return {'statusCode': 200, 'message': 'No S3 buckets found'}

    count_object(buckets)
    versioning_check(buckets)
    print("S3 object count and versioning check completed successfully.")
    
    return {
        'statusCode': 200,
        'message': 'Successfully completed'
    }
