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

Set `AWS_REGION` to the Region where Nova Lite is enabled, and set `BEDROCK_MODEL_ID` if you need a model ID other than `amazon.nova-lite-v1:0`. Do not put AWS access keys in `.env`; use the AWS SDK credential provider chain. For local development with an IAM user profile, run `aws configure --profile <profile>` once, then set `AWS_PROFILE=<profile>` in your shell before starting the server. With IAM Identity Center, run `aws sso login --profile <profile>` first. The identity needs `bedrock:InvokeModel` permission for the chosen model.

Start the API from the `backend/` directory:

```bash
uvicorn app.main:app --reload
```

- Health check: `GET http://localhost:8000/health`
- Interactive API docs: `http://localhost:8000/docs`
- Syllabus summary: `POST http://localhost:8000/api/v1/syllabi/summarize`

Example request:

```json
{
  "syllabus_text": "Paste syllabus text here",
  "course_name": "Example 101"
}
```

The summary endpoint sends the supplied text directly to Nova Lite using the Bedrock Runtime Converse API. The model is instructed to return structured JSON with syllabus details and important dates; the API currently returns that JSON as text in its `summary` field. Syllabus text is not stored, and dates are not yet converted into calendar events.

## Planned backend areas

- `app/api/routes/` — versioned HTTP endpoints.
- `app/core/` — application configuration.
- `app/models/` — validated API/domain models, including course and academic-event shapes.
- `app/services/` — integrations and business logic, including Bedrock.
- `app/repositories/` — future persistence boundary for syllabi, courses, and events.

No database, catalog data source, authentication, or file-upload flow is selected yet; choose those before implementing persistent calendar and degree-progress features.
