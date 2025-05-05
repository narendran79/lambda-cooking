# S3 Bucket Monitoring Lambda

**Overview:**
This Lambda function monitors S3 buckets for:
1. Object Count: Checks if any bucket exceeds a predefined object count limit. Sends an SNS alert if the limit is exceeded.
2. Versioning: Checks if versioning is enabled on the buckets. Sends an SNS alert if versioning is disabled.

The function is triggered by an EventBridge scheduler.

**Prerequisites:**
- Lambda Deployment: Deploy in AWS Lambda. Don't forget to set timeout to 10 sec in general configuration.
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

**Snapshot:**

1. EventBridge Schedular:
   
   <img width="801" alt="image" src="https://github.com/user-attachments/assets/b814158c-db38-420d-8063-ca1bd57b874b" />

2. Lambda Function:
   
   <img width="794" alt="image" src="https://github.com/user-attachments/assets/e19fa704-3e40-4b24-9111-85d9521df0f5" />

3. S3 Bucket:
   
   <img width="791" alt="image" src="https://github.com/user-attachments/assets/c6468c27-514a-4cf6-850a-d1d10955bfd3" />

4. SNS:
   
   <img width="804" alt="image" src="https://github.com/user-attachments/assets/d6e54f48-b2f1-4269-892a-9366050e4265" />

5. CloudWatch: (To monitor the logs)
   
   <img width="809" alt="image" src="https://github.com/user-attachments/assets/070aebbb-8199-4f02-a2dd-a087b3c88689" />


