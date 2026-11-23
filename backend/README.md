# Backend API

This document covers setup and use of the FastAPI backend. For the project overview, see the [main README](../README.md).

## Requirements

- Python 3.10 or newer
- AWS credentials with permission to invoke the selected Amazon Bedrock model
- Tesseract OCR for scanned PDFs (`brew install tesseract` on macOS)

## Local Setup

From the repository root, create a virtual environment and install the backend dependencies:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## AWS Configuration

The backend uses the AWS SDK credential provider chain. Do not put AWS access keys in `.env`.

For an IAM user profile, configure AWS once:

```bash
aws configure --profile <profile>
```

For IAM Identity Center, sign in with:

```bash
aws sso login --profile <profile>
```

Before starting the backend, select the profile in the same terminal:

```bash
export AWS_PROFILE=<profile>
```

In Windows PowerShell, use:

```powershell
$env:AWS_PROFILE = "<profile>"
```

The selected identity needs `bedrock:InvokeModel` permission for the chosen model. Set `AWS_REGION` to a Region where the model is available. The default model ID is `amazon.nova-lite-v1:0`; set `BEDROCK_MODEL_ID` to use a different model.

## Run the API

From the `backend/` directory, with the virtual environment active and AWS profile configured:

```bash
uvicorn app.main:app --reload
```

The service runs at `http://localhost:8000`.

## Endpoints

| Method and path | Purpose |
|---|---|
| `GET /health` | Check whether the API is running. |
| `POST /api/v1/syllabi/summarize` | Summarize syllabus text submitted as JSON. |
| `POST /api/v1/syllabi/summarize-batch` | Extract and summarize uploaded syllabus files. |

Interactive API documentation is available at `http://localhost:8000/docs` while the service is running.

### Text summary

Send a JSON request to `POST /api/v1/syllabi/summarize`:

```json
{
  "syllabus_text": "Paste syllabus text here",
  "course_name": "Example 101"
}
```

### Batch file summary

The batch endpoint accepts up to eight `.txt`, `.pdf`, or `.docx` files per request, with a maximum size of 15 MiB per file. It extracts text from each file and returns a structured summary with the upload index and filename. PDF pages with little extractable text are processed with local Tesseract OCR.

The API response is validated against the Pydantic schema. Uploaded files and extracted text are not stored.
