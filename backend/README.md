# Backend

FastAPI service that provides the API for syllabus summarization and, as the project grows, calendar and major-catalog features.

## Setup

Requires Python 3.10 or newer and AWS credentials authorized to invoke Amazon Nova Lite in Amazon Bedrock.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Scanned PDFs use local Tesseract OCR. On macOS, install the OCR engine with:

```bash
brew install tesseract
```

The Python PDF-rendering and OCR dependencies are installed by `requirements.txt`. OCR runs only on pages that contain little or no extractable text.

Set `AWS_REGION` to the Region where Nova Lite is enabled, and set `BEDROCK_MODEL_ID` if you need a model ID other than `amazon.nova-lite-v1:0`. Do not put AWS access keys in `.env`; use the AWS SDK credential provider chain. For local development with an IAM user profile, run `aws configure --profile <profile>` once, then set `AWS_PROFILE=<profile>` in your shell before starting the server. With IAM Identity Center, run `aws sso login --profile <profile>` first. The identity needs `bedrock:InvokeModel` permission for the chosen model.

Start the API from the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

- Health check: `GET http://localhost:8000/health`
- Interactive API docs: `http://localhost:8000/docs`
- Syllabus summary: `POST http://localhost:8000/api/v1/syllabi/summarize`
- Batch file summaries: `POST http://localhost:8000/api/v1/syllabi/summarize-batch`

Example request:

```json
{
  "syllabus_text": "Paste syllabus text here",
  "course_name": "Example 101"
}
```

The text summary endpoint sends the supplied text directly to Nova Lite using the Bedrock Runtime Converse API and returns a validated structured response.

The batch endpoint accepts up to eight `.txt`, `.pdf`, or `.docx` files per request, with a 15 MiB limit per file. It extracts text and summarizes each file separately, returning each result with its upload index and filename. For PDFs, pages with little or no extractable text are rendered and processed with local Tesseract OCR. Uploaded files and extracted text are not stored.

## Planned backend areas

- `app/api/routes/` — versioned HTTP endpoints.
- `app/core/` — application configuration.
- `app/models/` — validated API/domain models, including course and academic-event shapes.
- `app/services/` — integrations and business logic, including Bedrock.
- `app/repositories/` — future persistence boundary for syllabi, courses, and events.

No database, catalog data source, or authentication is implemented yet; choose those before implementing persistent calendar and degree-progress features.
