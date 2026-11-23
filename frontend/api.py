
#Loads library that lets python send messages to a web server.
import requests

#Backend connection
BASE_URL = "http://localhost:8000/api/v1/syllabi"
TIMEOUT_SECONDS = 120

def summarize_text(syllabus_text, course_name=None):
    response = requests.post(
        f"{BASE_URL}/summarize",
        json={"syllabus_text": syllabus_text, "course_name": course_name or None},
        timeout=TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()

def summarize_files(uploaded_files):
    files = []
    for f in uploaded_files:
        files.append(("files", (f.name, f.getvalue())))

    response = requests.post(
        f"{BASE_URL}/summarize-batch",
        files=files,
        timeout=TIMEOUT_SECONDS * len(uploaded_files),
    )
    response.raise_for_status()

    summaries = []
    for result in response.json()["results"]:
        summaries.append(result["summary"])
    return summaries