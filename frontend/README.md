# Syllabus Planner (Front End)

Upload your syllabi and get every due date from every class in one week-by-week calendar.

## What you need

- Python 3.10 or newer
- AWS access to Amazon Bedrock (Nova Lite), set up on your computer. Never put keys in the code or in `.env`.

## 1. Set up your AWS access (one time)

```bash
aws configure --profile myprofile
```

Type in your own Access Key ID, Secret Access Key, and Region when it asks.

## 2. Start the backend (Terminal 1)

```bash
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:AWS_PROFILE = "myprofile"
uvicorn app.main:app --reload
```

Leave this terminal open. Check that it works by opening http://localhost:8000/health

## 3. Start the front end (Terminal 2)

```bash
cd frontend
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app opens at http://localhost:8501

## 4. Use it

1. Upload one or more syllabi (`.pdf`, `.docx`, or `.txt`, up to 8 files).
2. Click **Build my planner**.
3. See all your dates laid out week by week.

## Files

| File | What it does |
|---|---|
| `app.py` | The page: upload box, button, calendar |
| `api.py` | Sends the files to the backend |
| `planner.py` | Combines, sorts, and groups dates by week |
| `display.py` | Draws the weekly calendar |

## Common problems

- **`streamlit` not recognized:** use `python -m streamlit run app.py`.
- **500 error:** the backend can't reach AWS. Check that `AWS_PROFILE` is set in Terminal 1 before running `uvicorn`.
- **Can't reach the backend:** make sure Terminal 1 is still running.
