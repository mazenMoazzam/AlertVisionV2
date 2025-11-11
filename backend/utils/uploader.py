import boto3
import os
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv("AWS_S3_BUCKET")

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def upload_to_s3(file_path, object_name=None):
    try:
        s3.upload_file(file_path, BUCKET_NAME, object_name or file_path)
        print(f"Uploaded {file_path} to S3 bucket: {BUCKET_NAME}")
    except Exception as e:
        print(f"Failed to upload {file_path}: {e}")
