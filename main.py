import os
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

def main():
    # 1. Retrieve environment variables provided by GitHub Actions
    creds_json_string = os.environ.get("AWS_CREDS_JSON")
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    
    if not creds_json_string or not bucket_name:
        print("Error: Missing required environment variables.")
        return

    try:
        # 2. Parse the secret JSON payload coming from Akeyless
        creds = json.loads(creds_json_string)
        aws_access_key = creds.get("username")
        aws_secret_key = creds.get("password")
        
    except json.JSONDecodeError:
        print("Error: Failed to parse Akeyless secret as JSON.")
        return

    if not aws_access_key or not aws_secret_key:
        print("Error: Extracted credentials are empty.")
        return

    # 3. Create a local text file containing the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = "demo-timestamp.txt"
    file_content = f"Deployment verified successfully via GitHub Actions and Akeyless!\nTimestamp: {current_time}\n"
    
    with open(file_name, "w") as file:
        file.write(file_content)
    print(f"Generated local file '{file_name}' with timestamp: {current_time}")

    # 4. Initialize Boto3 S3 client
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

    # 5. Check if the bucket exists, and create it if it does not
    try:
        print(f"Checking if S3 bucket '{bucket_name}' exists...")
        s3_client.head_bucket(Bucket=bucket_name)
        print(f"Bucket '{bucket_name}' already exists.")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"Bucket '{bucket_name}' does not exist. Attempting to create it...")
            try:
                # Create bucket (defaults to us-east-1 configuration)
                s3_client.create_bucket(Bucket=bucket_name)
                print(f"Successfully created new S3 bucket: '{bucket_name}'")
            except ClientError as ce:
                print(f"Failed to create bucket: {ce}")
                return
        else:
            print(f"Unexpected AWS error when checking bucket: {e}")
            return

    # 6. Upload the generated timestamp file to your AWS S3 bucket
    try:
        print(f"Uploading '{file_name}' to S3 bucket '{bucket_name}'...")
        s3_client.upload_file(file_name, bucket_name, file_name)
        print("Success! The timestamp file has been uploaded and will persist in AWS.")
    except ClientError as e:
        print(f"AWS ClientError during upload: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
