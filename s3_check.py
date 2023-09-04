import os
import boto3

s3 = boto3.client('s3')

bucket = os.environ.get('AWS_S3_BUCKET')

response = s3.list_objects_v2(Bucket=bucket)

for obj in response['Contents']:
    print(obj['Key'])