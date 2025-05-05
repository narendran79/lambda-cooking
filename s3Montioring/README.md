# S3 Bucket Monitoring Lambda

**Overview:**
This Lambda function monitors S3 buckets for:
1. Object Count: Checks if any bucket exceeds a predefined object count limit. Sends an SNS alert if the limit is exceeded.
2. Versioning: Checks if versioning is enabled on the buckets. Sends an SNS alert if versioning is disabled.

The function is triggered by an EventBridge scheduler.

**Prerequisites:**
- Lambda Deployment: Deploy in AWS Lambda.
- SNS Topic: Create an SNS topic (`mys3objectalert`) for email alerts.
- IAM Role: Lambda needs permissions for `s3:ListAllMyBuckets`, `s3:GetBucketVersioning`, and `sns:Publish`.
- EventBridge schedular: Schedule the Lambda to run periodically.

**Configuration:**
- TOPIC_ARN: SNS topic ARN for alerts (replace with your ARN).
- OBJECT_COUNT_LIMIT: Set the object count threshold for alerts (default is 5).

**Function Flow:**
1. Triggered by EventBridge.
2. Lists all S3 buckets.
3. Performs the object count check and versioning check for each bucket.
4. Sends SNS alerts if conditions are met.

**Example Alerts:**
Object Count Alert:
Alert From S3 !!!
Bucket "example-bucket" exceeded the object count limit of 5.
Please delete unused objects.

**Versioning Alert:**
Alert From S3 !!!
Versioning is DISABLED on bucket "example-bucket".
Please enable versioning.

**Troubleshooting:**
- No Buckets: Ensure the Lambda has permission (`s3:ListAllMyBuckets`).
- SNS Issue: Check SNS topic ARN and Lambda permissions (`sns:Publish`).

**Deployment Steps:**
1. Deploy Lambda.
2. Set up EventBridge trigger.
3. Ensure IAM permissions are correctly set.
