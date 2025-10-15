## Compliant HLS Streamer (User/Public-Domain Content)

### Prerequisites
- Python 3.10+
- Node 18+
- FFmpeg in PATH (`ffmpeg -version`)

### Backend
```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Endpoints:
- POST `/upload` → { movie_id, manifest }
- POST `/cleanup/{movie_id}`
- GET `/health`
- Static HLS served at `/media/{movie_id}/index.m3u8`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Configure `VITE_BACKEND_URL` in a `.env` file under `frontend/` if backend is remote.

### Notes
- Uploaded files are converted to HLS segments and manifest under `temp/hls/{movie_id}` and auto-swept after inactivity.
- Use only content you own or content in the public domain.


