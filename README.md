# B12 Application Submission Automator

This repository contains a specialized Python utility designed to automate the B12 application process via a CI/CD pipeline. The project demonstrates secure payload signing, JSON canonicalization, and automated workflow integration.

## Overview

The core of this project is a Python script (`submit_application.py`) that executes within a GitHub Actions environment. Upon a push to the `main` branch, the script:

1. Gathers metadata about the current GitHub Action run.
2. Canonicalizes the data into a strict JSON format.
3. Generates an **HMAC-SHA256 signature** for security.
4. Submits the payload to the B12 submission endpoint.

## Technical Implementation

To meet the strict requirements of the B12 API, the script implements the following:

* **JSON Canonicalization**: Uses `json.dumps` with `sort_keys=True` and `separators=(',', ':')` to ensure a compact, predictable payload format with no extra whitespace.
* **Security**: Implements HMAC-SHA256 signing. The raw UTF-8 encoded body is signed using a secret key, and the resulting hex digest is passed in the `X-Signature-256` header.
* **CI/CD Integration**: Fully integrated with GitHub Actions using environment variables (`GITHUB_RUN_ID`, `GITHUB_REPOSITORY`) to dynamically generate submission links.

## Setup & Installation

### Local Development

If you wish to run the script locally for testing:

1. **Clone the repository**:
```bash
git clone https://github.com/neelxie/b12.git
cd submit

```


2. **Install dependencies**:
```bash
pip install -r requirements.txt

```


3. **Run the script**:
*(Note: You will need to set dummy environment variables for local runs)*
```bash
export GITHUB_REPOSITORY="user/repo"
export GITHUB_RUN_ID="12345"
python submit_application.py

```



### GitHub Actions Configuration

To enable the automated submission:

1. Go to your repository **Settings** > **Secrets and variables** > **Actions**.
2. Add a new repository secret named `B12_SECRET`.
3. Set the value to `hello-there-from-b12`.

## Project Structure

```text
.
├── .github/workflows/
│   └── submit.yml          # GitHub Action definition
├── submit_application.py   # Main submission logic
├── requirements.txt        # Python dependencies
├── .gitignore              # Standard Python git exclusions
└── README.md               # Documentation

```

##  License

This project is for application purposes and is open-source under the MIT License.
