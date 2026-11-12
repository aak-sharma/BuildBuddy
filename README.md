# BuildBuddy – CI/CD Build Log Analyzer

BuildBuddy is a beginner-friendly developer tool that analyzes common CI/CD build logs. It detects familiar error patterns, explains what they usually mean, and suggests practical troubleshooting steps.

It is designed as a small portfolio project related to Harness's Software Engineering / Forward Deployed Engineering internship focus areas: CI/CD, debugging, root-cause analysis, developer tooling, APIs, and applied AI.

## Features

- Paste a build log or upload a `.log` / `.txt` file.
- Detect common dependency, syntax, test, Docker, configuration, and network errors.
- Show the matched log evidence, a plain-English explanation, and suggested next steps.
- Try the included sample logs.
- Optionally request an additional explanation using the Gemini API.
- Download findings as a JSON file.
- Run automated tests with pytest.
- Run a GitHub Actions workflow on pushes and pull requests.

**Important:** BuildBuddy does not change source code, apply fixes, or deploy applications. It is a diagnostic helper. Always review the original logs and validate suggested fixes yourself.

---

## 1. Requirements

Install the following:

- Python 3.10 or newer (Python 3.11 is recommended).
- pip (usually installed with Python).
- Git (optional, but recommended for pushing the project to GitHub).
- A code editor such as VS Code.

Check your Python installation:

```bash
python --version
pip --version
```

On some Windows systems, use `py` instead of `python`.

## 2. Download and extract the project

1. Download `BuildBuddy.zip`.
2. Extract it to a folder, for example `C:\Projects\BuildBuddy`.
3. Open that folder in VS Code.
4. Open the VS Code terminal: **Terminal → New Terminal**.

The folder should look like this:

```text
BuildBuddy/
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── github_client.py
│   └── main.py
├── sample_logs/
│   ├── docker_failure.log
│   ├── failed_tests.log
│   └── missing_dependency.log
├── tests/
│   └── test_analyzer.py
├── .github/
│   └── workflows/
│       └── tests.yml
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 3. Create a virtual environment

In the terminal, make sure you are inside the `BuildBuddy` folder.

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run this command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

When activated, you should see `(.venv)` at the start of the terminal prompt.

## 4. Install dependencies

Run:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The core analyzer works without an AI API key. The Gemini package is included so you can enable the optional AI explanation.

If installation fails, confirm that the virtual environment is activated and that you are using Python 3.10 or newer.

## 5. Run BuildBuddy locally

From the project root, run:

```bash
streamlit run app/main.py
```

Streamlit should open the application in your browser, usually at:

```text
http://localhost:8501
```

If it does not open automatically, copy that address into your browser.

### Try the sample logs

1. Choose **Missing dependency** from the sample dropdown.
2. Click **Analyze build log**.
3. Review the category, matched evidence, explanation, and suggested fix.
4. Repeat with **Failed tests** and **Docker build failure**.
5. You can also paste your own CI/CD log or upload a `.log` / `.txt` file.
6. Use **Download analysis as JSON** to save the findings.

You can stop the local server by pressing `Ctrl + C` in the terminal.

## 6. Enable optional Gemini AI explanations

The AI feature is optional. The rule-based analyzer works without it.

1. Create or access a Gemini API key through Google AI Studio.
2. Copy `.env.example` and rename the copy to `.env`.
3. Open `.env` and add your key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

4. Save the file.
5. Restart the Streamlit app if it is already running.
6. In the BuildBuddy sidebar, turn on **Add AI explanation**.
7. The key should be loaded from `.env`. You can also paste a key directly into the password field.

Never upload your `.env` file to GitHub or share your API key. The `.gitignore` file is configured to ignore `.env`.

If the AI provider is unavailable or the key is invalid, BuildBuddy still displays its rule-based findings.

## 7. Run automated tests

With the virtual environment activated, run:

```bash
pytest -q
```

The included tests check that BuildBuddy can identify a missing dependency, detect a failed test, handle an unknown log, and summarize severity counts.

## 8. GitHub Actions CI workflow

The project includes:

```text
.github/workflows/tests.yml
```

This workflow:

1. Starts an Ubuntu runner.
2. Checks out the repository.
3. Sets up Python 3.11.
4. Installs the project requirements.
5. Runs `pytest -q`.

### Push the project to GitHub

Create an empty repository on GitHub, then run these commands from the project folder:

```bash
git init
git add .
git commit -m "Initial BuildBuddy project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/BuildBuddy.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username and use your actual repository URL.

Open the repository on GitHub and select **Actions** to see the workflow run. You can also make a small code change and push it to trigger another run.

## 9. Project structure explained

| File | Purpose |
|---|---|
| `app/main.py` | Streamlit user interface and application flow |
| `app/analyzer.py` | Rule-based error detection and optional Gemini explanation |
| `app/github_client.py` | Optional helper for retrieving recent GitHub Actions runs |
| `tests/test_analyzer.py` | Automated tests for the analyzer |
| `.github/workflows/tests.yml` | GitHub Actions CI workflow |
| `sample_logs/` | Example logs to test the app |
| `requirements.txt` | Python package dependencies |
| `.env.example` | Example environment variable file |

## 10. Troubleshooting

### `streamlit` is not recognized

Activate the virtual environment and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app/main.py
```

### `ModuleNotFoundError`

Check that the virtual environment is active, then run:

```bash
python -m pip install -r requirements.txt
```

Run commands from the main `BuildBuddy` folder, not from inside `app`.

### Port 8501 is already in use

Use another port:

```bash
streamlit run app/main.py --server.port 8502
```

### Gemini explanation is unavailable

Check that the API key is valid, that `.env` is in the project root, and that the environment variable is named exactly `GEMINI_API_KEY`. The basic analyzer does not require Gemini.

### GitHub Actions workflow is not visible

Make sure `.github/workflows/tests.yml` was committed and pushed to the default branch. Check the repository's **Actions** tab.

## 11. Limitations and responsible use

- Pattern matching recognizes common errors; it cannot diagnose every possible build failure.
- AI output can be incorrect. Validate suggestions before applying them.
- Logs can contain passwords, tokens, private URLs, or customer data. Redact sensitive values before uploading.
- The optional GitHub helper makes a read-only request for workflow run information; it is not currently connected to the Streamlit interface.
- BuildBuddy does not automatically commit changes, create pull requests, or deploy applications.

## 12. Possible future improvements

- Add more error signatures and configurable rules.
- Connect the GitHub Actions helper to the dashboard.
- Add filters for workflow status and branch.
- Store analysis history in SQLite.
- Add Docker packaging.
- Add Bandit security scanning.

## 13. Resume description

**BuildBuddy – CI/CD Build Log Analyzer**  
*Python, Streamlit, Regex, Gemini API, GitHub Actions, Pytest*

- Developed a Streamlit-based tool to analyze CI/CD build logs and identify common dependency, syntax, testing, Docker, and configuration errors.
- Implemented rule-based error classification with matched log evidence, root-cause explanations, and actionable troubleshooting suggestions.
- Integrated an optional Gemini API feature to generate additional natural-language explanations for build failures.
- Configured a GitHub Actions workflow to install dependencies and execute automated tests on pushes and pull requests.

Only include the Gemini integration and other features on your resume after you have tested them yourself.


## 14. Deploy BuildBuddy on Render

The easiest portfolio deployment is a Render web service.

1. Push the project to a GitHub repository (see section 8).
2. Sign in to Render and choose **New → Web Service**.
3. Connect your GitHub account and select the `BuildBuddy` repository.
4. Use these settings:
   - **Runtime:** Python
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `streamlit run app/main.py --server.address 0.0.0.0 --server.port $PORT`
5. Choose an available instance plan and click **Deploy**.
6. When deployment finishes, open the Render URL shown on the service page.

### Add the Gemini key on Render (optional)

In your Render service, open **Environment** and add:

- Key: `GEMINI_API_KEY`
- Value: your Gemini API key

Save the changes and redeploy. Never place the key in source code or commit `.env`.

Note: free hosting availability, sleep behavior, and limits can change. Check the current Render plan details before selecting a plan. The app can still run without Gemini.

## 15. GitHub push checklist

Before pushing:

- Confirm `.env` is not staged or committed.
- Confirm `.gitignore` contains `.env`.
- Run `python -m pytest -q`.
- Run the app locally and test all three sample logs.
- Push the `.github/workflows/tests.yml` workflow.
- Confirm the Actions tab shows a successful test run.

## 16. Resume link

After deployment, add the public Render URL to your resume and GitHub repository description. Include only features you personally tested.
