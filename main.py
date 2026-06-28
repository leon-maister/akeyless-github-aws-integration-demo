import os
import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

def main():
    creds_json_string = os.environ.get("AWS_CREDS_JSON")
    bucket_name = os.environ.get("S3_BUCKET_NAME")
    
    if not creds_json_string:
        print("❌ Error: AWS_CREDS_JSON environment variable is completely empty!")
        return

    # 🛑 DEBUG: Print the raw content of the secret to see its format
    print("================ RAW SECRET DEBUG ================")
    print(f"Secret data type: {type(creds_json_string)}")
    print(f"Secret character length: {len(creds_json_string)}")
    print(f"Raw Secret Content:\n{creds_json_string}")
    print("==================================================")
    
    try:
        creds = json.loads(creds_json_string)
        print(f"Debug: Available JSON keys: {list(creds.keys())}")
        
        # Checking both lowercase and uppercase variations
        aws_access_key = creds.get("aws_access_key_id") or creds.get("AWS_ACCESS_KEY_ID")
        aws_secret_key = creds.get("aws_secret_access_key") or creds.get("AWS_SECRET_ACCESS_KEY")
        aws_session_token = creds.get("aws_session_token") or creds.get("AWS_SESSION_TOKEN", None)
    except json.JSONDecodeError:
        print("❌ Notice: Secret is not a standard JSON object. Treating as plain text or malformed JSON.")
        return

    if not aws_access_key or not aws_secret_key:
        print("❌ Error: Could not extract access_key or secret_key from JSON.")
        return

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = "demo-timestamp.txt"
    file_content = f"Deployment verified successfully via GitHub Actions and Akeyless!\nTimestamp: {current_time}\n"
    
    with open(file_name, "w") as file:
        file.write(file_content)

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token
    )

    try:
        print(f"Uploading '{file_name}' to S3 bucket '{bucket_name}'...")
        s3_client.upload_file(file_name, bucket_name, file_name)
        print("Success! The timestamp file has been uploaded.")
    except ClientError as e:
        print(f"AWS ClientError during upload: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
