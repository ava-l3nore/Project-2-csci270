# Project 2: Student Study Planner

## 1. What

The Student Study Planner is an AI-powered application for turning course syllabi into useful academic planning information. It extracts course details and important dates, and presents syllabus events in a calendar.

The project has two main components:

- **Frontend:** A Streamlit application for uploading syllabi and viewing extracted events in month or week-by-week calendar views. See the [frontend README](./frontend/README.md) for setup and usage.
- **Backend:** A FastAPI service that extracts and summarizes syllabus content using Amazon Nova Lite through Amazon Bedrock. See the [backend README](./backend/README.md) for API details and setup.

## 2. How

Users upload syllabus files through the frontend. The frontend sends them to the backend, which extracts text from supported documents and uses Amazon Nova Lite to identify course information and important dates. The structured response is then shown in the planner calendar.

For scanned PDF pages, the backend can use local Tesseract OCR. The backend currently accepts `.txt`, `.pdf`, and `.docx` files, up to eight files per request and 15 MiB per file.

To run the application locally, start the backend and frontend in separate terminals. Follow the setup instructions in the [backend README](./backend/README.md) and [frontend README](./frontend/README.md).

## 3. Why

Course requirements and deadlines are often spread across long syllabi and presented in different formats. This project is intended to make that information easier to find and help students see important academic dates across their courses in one place.

## 4. When

Use the planner when organizing coursework or reviewing upcoming syllabus dates. The backend must be running while using frontend features that submit syllabi for summarization.

## 5. Future Work

- **Work Schedule Integration** — Allow students to add work commitments to the calendar for more accurate and balanced planning.
- **Dynamic Academic Calendars** — Enable calendar views to automatically update according to the selected academic year or semester.
- **Study Session Scheduling** — Allow users to create study sessions and add them directly to the calendar.
- **Degree Progress Tracking** — Track required courses and progress toward graduation for a student's selected major.


## Project Structure

- `backend/` — FastAPI API, document text extraction, and Amazon Bedrock integration.
- `frontend/` — Streamlit application and calendar views.
