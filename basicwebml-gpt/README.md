# BasicWebML-GPT

A minimal template for building a plugin-based GPT web interface using FastAPI and React.

## Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend

Placeholder React setup. See `frontend/` directory.

### Plugins

Add plugins in `backend/plugins/`. Each plugin exposes `get_metadata()` and `predict()`.
Reload plugins by calling `POST /api/v1/plugins/refresh`.

### Threads

Run multiple conversations simultaneously. Use `POST /api/v1/threads` to create a thread and `POST /api/v1/threads/<id>/messages` to send prompts. Archives can be downloaded via `/api/v1/threads/<id>/archive`.
