import os
import boto3
from botocore.exceptions import ClientError

# 1. Configure the S3 client pointing to the Floci endpoint
s3_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:4566",  # Redirects to Floci
    aws_access_key_id="mock_key",
    aws_secret_access_key="mock_secret",
    region_name="us-east-1",
)

# Define the names of the resources (created by your Terraform)
SOURCE_BUCKET = "my-local-bucket-1"
TARGET_BUCKET = "my-local-bucket-2"
LOCAL_FILE = "local_file.txt"
SOURCE_NAME = "source_file.txt"
TARGET_NAME = "target_file.txt"

# Create a test file locally if it doesn't exist
if not os.path.exists(LOCAL_FILE):
    with open(LOCAL_FILE, "w", encoding="utf-8") as f:
        f.write("Test content for Floci S3 validation.")

try:
    # ---- STEP A: Upload the file to Bucket 1 ----
    print(f"Uploading {LOCAL_FILE} to bucket '{SOURCE_BUCKET}'...")
    s3_client.upload_file(LOCAL_FILE, SOURCE_BUCKET, SOURCE_NAME)
    print("Upload completed successfully!")

    # ---- STEP B: Copy the file to Bucket 2 with a new name ----
    print(
        f"\nCopying and renaming from '{SOURCE_BUCKET}/{SOURCE_NAME}' to '{TARGET_BUCKET}/{TARGET_NAME}'..."
    )

    # The S3 requires the source structure as a dictionary or specific string
    source_structure = {"Bucket": SOURCE_BUCKET, "Key": SOURCE_NAME}

    s3_client.copy(CopySource=source_structure, Bucket=TARGET_BUCKET, Key=TARGET_NAME)
    print("Copy and rename completed successfully!")

    # ---- VALIDATION: List the files in the Destination Bucket ----
    print(f"\n--- Files in bucket {TARGET_BUCKET} ---")
    response = s3_client.list_objects_v2(Bucket=TARGET_BUCKET)
    if "Contents" in response:
        for item in response["Contents"]:
            print(f"-> Name: {item['Key']} | Size: {item['Size']} bytes")
    else:
        print("The destination bucket is empty.")

except ClientError as e:
    print(f"An error occurred in the S3 API: {e}")
