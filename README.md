# Akeyless GitHub Actions & AWS S3 Integration Demo

This repository demonstrates how to securely retrieve AWS credentials from Akeyless using GitHub Actions OIDC (JWT) authentication and deploy a timestamp verification file to an Amazon S3 bucket.

### 🎯 Project Goal
**The primary goal of this project is to eliminate hardcoded cloud credentials in CI/CD pipelines by leveraging a keyless connection between GitHub Actions and Akeyless.**

### 🧩 Process Decomposition

#### Phase 1: Authentication & Secrets Fetch
1. **OIDC Handshake**: GitHub Actions generates a short-lived, cryptographically signed OIDC JWT token.
2. **Akeyless Validation**: The Akeyless Github Action sends this token to the Akeyless API, verifying the GitHub repository identity.
3. **Secure Retrieval**: Upon successful authentication, Akeyless securely returns the AWS credentials payload (JSON) to the runner memory.

#### Phase 2: Application Logic & AWS Deployment
1. **Credential Parsing**: The Python script parses the Akeyless secret JSON, extracting the dynamic AWS Access Key and Secret Key.
2. **State Verification**: The script checks if the target S3 bucket exists within the specified AWS region, automatically creating it if it is missing.
3. **Artifact Persistence**: A local text file containing a valid GMT timestamp is generated and uploaded directly to the AWS S3 bucket.

## 📂 Core Components
| File | Function |
| :--- | :--- |
| .github/workflows/aws-demo.yml | **GitHub Pipeline**: Orchestrates OIDC auth with Akeyless and sets environment variables. |
| main.py | **Python Application**: Parses fetched credentials, manages S3 buckets, and handles file uploads via boto3. |

## ⚙️ Configuration Variables
The following pipeline variables are utilized within the environment:

### GitHub Actions Inputs
- `bucket_name`: Name of the target AWS S3 bucket (Default: `leon-akeyless-github-plugin-aws-integration-demo-bucket`).

### Application Runtime Environments
- `AWS_CREDS_JSON`: Raw JSON string from Akeyless containing cloud access keys.
- `AWS_DEFAULT_REGION`: Target AWS deployment region (Configured to `us-east-2`).

## 🚀 Usage
1. Push changes to the repository or manually trigger the workflow from the GitHub Actions tab.
2. Provide a custom S3 bucket name if needed, then run the workflow.
3. Monitor execution and verify the presence of `demo-timestamp.txt` in your AWS S3 console.

---
**Maintained by**: [leon-maister](https://github.com/leon-maister)

<sub style="color: gray;">/home/keyless/PluginDemo</sub>
