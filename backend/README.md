## Backend (FastAPI)

### Setup
1. Create a virtual environment and install deps:
```bash
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
```

2. Create `.env` based on `.env.example`.

3. Run dev server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Env Vars
- TELEGRAM_API_ID
- TELEGRAM_API_HASH
- TELEGRAM_BOT_TOKEN (optional)
- TELEGRAM_SEARCH_CHATS (comma-separated)
- CORS_ALLOW_ORIGINS (default `*`)
- TEMP_DIR (default `temp`)
- HLS_DIRNAME (default `hls`)
- CLEANUP_AFTER_SECONDS (default `3600`)
