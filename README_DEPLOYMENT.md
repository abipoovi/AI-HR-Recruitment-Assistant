# AI HR Recruitment Assistant — Updated Cloud Model Setup

This version replaces local Ollama/Qwen with the Groq cloud API. The Flask app serves both the HTML frontend and API from the same origin, so the browser's `fetch("/analyze")` request works without a separate frontend API URL.

## 1. Requirements

- Python 3.11 recommended
- A Groq API key: https://console.groq.com/keys

## 2. Run locally (Windows)

1. Extract the project ZIP and open this folder in VS Code.
2. Open a terminal in the project folder.
3. Create a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .venv\Scripts\activate
   ```

4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Copy `.env.example` to `.env` and replace the placeholder with your real key:

   ```env
   GROQ_API_KEY=your_real_key_here
   GROQ_MODEL=openai/gpt-oss-20b
   ```

6. Start the application:

   ```powershell
   python server.py
   ```

7. Open http://127.0.0.1:5000 and test `/health` at http://127.0.0.1:5000/health.

## 3. Deploy the complete app on Render

Deploy this repository as one Render Web Service (not a separate static Vercel site for this Flask-served frontend). The Flask server serves `templates/index.html`, `static/style.css`, and `static/script.js`, and also handles `/analyze`. Keeping them on one origin avoids the common frontend/backend connection error.

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn server:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
- Health check path: `/health`
- Environment variables: `GROQ_API_KEY` (secret), `GROQ_MODEL` = `openai/gpt-oss-20b`

The included `render.yaml` provides these settings. Add the secret key in Render's Environment settings; do not commit `.env`.

## 4. Model selection

The default is `openai/gpt-oss-20b`. You can change `GROQ_MODEL` to another model ID currently listed in https://console.groq.com/docs/models. The API key must have access to the selected model.

## 5. Important notes

- Ollama does not need to be installed or running.
- Never paste your API key into JavaScript, HTML, GitHub, or screenshots.
- `/health` checks that Flask is running and reports whether the key is configured; it does not spend tokens by calling the model.
- Candidate match scores are rule-based skill overlap and should be treated as decision support, not an automated hiring decision.
