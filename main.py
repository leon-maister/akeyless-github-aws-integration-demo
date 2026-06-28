name: AWS Integration Demo via Akeyless

on:
  workflow_dispatch:
    inputs:
      bucket_name:
        description: 'Target S3 bucket name'
        required: true
        # Added 'leon-' prefix as requested
        default: 'leon-akeyless-demo-bucket-unique-2026'

jobs:
  deploy-to-s3:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - name: Checkout repository code
        uses: actions/checkout@v4

      - name: Fetch AWS credentials from Akeyless
        uses: akeyless-community/akeyless-github-action@v1.1.2
        id: fetch-secrets
        with:
          access-id: p-fm7yoqdlm4voom
          access-type: jwt
          api-url: https://api.akeyless.io
          static-secrets: |
            - name: "/Demo/GitHubPlugin-AWS-Integration/AWS-creds"
              output-name: "aws_credentials_json"

      - name: Set up Python environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install required Python dependencies
        run: pip install boto3

      - name: Generate timestamp file and upload to AWS S3
        env:
          AWS_CREDS_JSON: ${{ steps.fetch-secrets.outputs.aws_credentials_json }}
          S3_BUCKET_NAME: ${{ inputs.bucket_name }}
        run: python main.py
