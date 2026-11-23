# Syllabus Planner (Front End)

Upload your syllabi and see every exam, quiz, and deadline from every class on one calendar (month view or week by week).

## What you need

- Python 3.10 or newer
- Git and the AWS CLI
- AWS access to Amazon Bedrock (Nova Lite) through an AWS profile. Never put keys in the code or in `.env`.
- For scanned PDFs: Tesseract (`brew install tesseract` on macOS)

## 1. Get the code

```bash
git clone https://github.com/ava-l3nore/Project-2-csci270.git
cd Project-2-csci270
git checkout streamlit-calendar
```

If you already have the repo: `git fetch` then `git checkout streamlit-calendar` and `git pull`.

## 2. Install (one time)

From the repo root, create one virtual environment and install both sets of requirements:

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt -r frontend/requirements.txt
cp backend/.env.example backend/.env
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt -r frontend\requirements.txt
copy backend\.env.example backend\.env
```

## 3. Set up AWS access (one time)

```bash
aws configure --profile <your-profile>
```

Enter the Access Key ID, Secret Access Key, and Region (`us-east-1`) you were given. Ask the team which profile/credentials to use.

## 4. Start the backend (Terminal 1)

The AWS profile only lasts for the terminal you set it in, so set it every time you open a new terminal.

**macOS / Linux**
```bash
cd Project-2-csci270
source .venv/bin/activate
export AWS_PROFILE=<your-profile>
cd backend
uvicorn app.main:app --reload
```

**Windows (PowerShell)**
```powershell
cd Project-2-csci270
.venv\Scripts\Activate.ps1
$env:AWS_PROFILE = "<your-profile>"
cd backend
uvicorn app.main:app --reload
```

Wait for `Application startup complete.` and leave this terminal open. Check http://localhost:8000/health

## 5. Start the front end (Terminal 2)

```bash
cd Project-2-csci270
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
cd frontend
python -m streamlit run app.py
```

The app opens at http://localhost:8501

## 6. Test it

1. Upload one or more syllabi from the `Syllabi/` folder (up to 8 files, 15 MB each).
2. Click **Build my planner**.
3. Use **Month** or **Week by week**. Click an event in Month view to see its details and syllabus excerpt.
4. Open **Debug report** at the bottom to see exactly what the backend returned for each course.

Good test files: `Syllabus Spring2026 JPNS202-8.pdf`, `syllabus_250_01-1.pdf`, `COMM 104 Syllabus-1.pdf`.

What to expect: exams, quizzes, and most deadlines appear with correct dates. The month view opens on the earliest event (MATH 250 is Fall 2025), so click forward to reach 2026. Results vary a little between runs because the AI model isn't deterministic.

Known limitations:
- Homework and multi-day presentation days are often missed.
- A few dates can be off by a day or two, because PDF schedule tables get scrambled when the text is extracted.
- `French202_syllabus.pdf` never states a year, so its dates can come back wrong.
- `103 Fall 2026-syllabus-final.pdf` is over the 15 MB limit and will fail the upload.
- `CSCI_270_Fall2026_Syllabus.pdf` and `FREN336_Syllabus.pdf` are scans and need Tesseract installed.

## Files

| File | What it does |
|---|---|
| `app.py` | The page: upload box, button, Month/Week toggle, debug report |
| `api.py` | Sends the files to the backend |
| `planner.py` | Combines and sorts dates, fills in missing years from the course term, groups by week, builds calendar events |
| `display.py` | Draws the month calendar (streamlit-calendar) and the week-by-week view |

## Common problems

| Message | Fix |
|---|---|
| `Connection refused` / can't reach the backend | Terminal 1 isn't running. Start it again (step 4). |
| `NoCredentialsError: Unable to locate credentials` (in Terminal 1) | `AWS_PROFILE` isn't set in this terminal. Set it and restart `uvicorn`. |
| `500 Server Error` in the app | Read the last line of Terminal 1. If it says the response "does not match the syllabus schema", the AI returned bad output; click **Build my planner** again. |
| `streamlit` not recognized | Use `python -m streamlit run app.py`. |
| Terminal stuck showing a `:` prompt after a git command | Press `q`. |