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
        print("Error: Missing required environment variables (AWS_CREDS_JSON or S3_BUCKET_NAME).")
        return

    # 2. Parse AWS credentials from the Akeyless JSON output
    try:
        creds = json.loads(creds_json_string)
        aws_access_key = creds.get("aws_access_key_id")
        aws_secret_key = creds.get("aws_secret_access_key")
        # Optional: handle session token if it's a dynamic or temporary credential
        aws_session_token = creds.get("aws_session_token", None)
    except json.JSONDecodeError:
        print("Error: Failed to parse Akeyless secret as JSON. Check the secret format.")
        return

    # 3. Create the text file containing the current date and time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = "demo-timestamp.txt"
    file_content = f"Deployment verified successfully via GitHub Actions and Akeyless!\nTimestamp: {current_time}\n"
    
    with open(file_name, "w") as file:
        file.write(file_content)
    print(f"Generated local file '{file_name}' with timestamp: {current_time}")

    # 4. Initialize Boto3 S3 client with extracted credentials
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token
    )

    # 5. Upload the generated file to the designated S3 bucket
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
