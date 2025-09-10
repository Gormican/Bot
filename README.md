# Personal Agent (clean baseline)

## Run locally
```bash
python -m venv .venv
. .venv/Scripts/activate  # Windows
pip install -r requirements.txt
set OPENAI_API_KEY=sk-your-key   # or put it in .env and load yourself
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/ui

## ENV
- `OPENAI_API_KEY`: required for /study/ask and /report/morning/speak

## Notes
- Prefs are stored in `app/data/prefs.json` (ephemeral on Render’s free tier).
- Home can be saved via ZIP only; lat/lon optional.
- Calendar uses your secret ICS URL (Google Calendar -> Settings -> your calendar -> Integrate -> Secret address in iCal).
"# Bot" 
"# Bot" 
