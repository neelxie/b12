import os
import json
import hmac
import hashlib
import requests
from datetime import datetime, timezone

def submit_application():
    # Configuration - with environment variables 
    url = "https://b12.io/apply/submission"
    secret = os.getenv("B12_SECRET", "hello-there-from-b12")
    # intentionally skipped fast fail if secret is not set for demo purposes
    
    # GitHub provides these default environment variables
    repo_name = os.getenv("GITHUB_REPOSITORY")
    run_id = os.getenv("GITHUB_RUN_ID")
    server_url = os.getenv("GITHUB_SERVER_URL", "https://github.com")

    # Building the payload
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace("+00:00", "Z"),
        "name": "Derrick Mukisa",
        "email": "kidricederek@gmail.com",
        "resume_link": "https://docs.google.com/document/d/1WN2DXUqi2lirVSliNNqKkxYQgCeNSI3Fe8f6W4m-jVM/edit?usp=sharing",
        "repository_link": f"{server_url}/{repo_name}",
        "action_run_link": f"{server_url}/{repo_name}/actions/runs/{run_id}"
    }

    # Canonicalize JSON: No extra whitespace, sorted keys, UTF-8
    body = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    body_bytes = body.encode('utf-8')

    # we then generate HMAC-SHA256 Signature
    signature = hmac.new(
        secret.encode('utf-8'),
        body_bytes,
        hashlib.sha256
    ).hexdigest()

    digest = hmac.new(
      secret.encode('utf-8'),
      body_bytes,
      hashlib.sha256
    ).hexdigest()

    print(f"Generated Digest: {digest}")

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256": f"sha256={signature}"
    }

    response = requests.post(url, data=body_bytes, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print(f"Submission Successful!")
        print(f"Receipt: {data.get('receipt')}")
    else:
        print(f"Failed with status {response.status_code}")
        print(response.text)
        exit(1)

if __name__ == "__main__":
    submit_application()