# Project 2

An AI study-planning tool for summarizing course syllabi, tracking important dates, and helping students compare their coursework with major requirements.

## Project layout

- `backend/` — API and server-side integrations. See [backend/README.md](./backend/README.md) for setup.
- `frontend/` — student-facing application (to be planned).

The backend currently provides a health check and a syllabus summarization endpoint that calls Amazon Nova Lite directly through Amazon Bedrock Runtime. Calendar persistence, catalog ingestion, and degree-progress planning are future work.