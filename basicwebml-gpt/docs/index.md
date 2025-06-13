# Documentation

This project demonstrates a plugin-driven machine learning web interface built with FastAPI and React.

## Writing Plugins

Create a new file in `backend/plugins/` that defines a `Plugin` class with `get_metadata()` and `predict()` methods.

Example:

```python
class Plugin:
    def get_metadata(self):
        return {"name": "my_plugin", "description": "What it does", "type": "demo"}

    def predict(self, prompt: str) -> str:
        return "..."
```

Reload plugins via:

```bash
curl -X POST http://localhost:8000/api/v1/plugins/refresh
```

## API Usage

- `POST /api/v1/generate` with JSON `{ "model": "basic_gpt", "prompt": "hi" }`
- `GET /api/v1/plugins` returns loaded plugin metadata
- `POST /api/v1/plugins/refresh` reloads plugins from disk

## Setup

```
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

## Threads and Archives

Each conversation is stored as a thread. Create a thread via:

```bash
curl -X POST http://localhost:8000/api/v1/threads -d '{"name": "session"}' -H 'Content-Type: application/json'
```

Send messages to a thread:

```bash
curl -X POST http://localhost:8000/api/v1/threads/<thread_id>/messages -d '{"model": "basic_gpt", "prompt": "hi"}' -H 'Content-Type: application/json'
```

List threads with `GET /api/v1/threads`. Threads can be renamed with `PUT /api/v1/threads/<id>` and deleted with `DELETE /api/v1/threads/<id>`.

Download an archive of a thread with `GET /api/v1/threads/<id>/archive`.

## Shared Cache

The shared cache holds facts or entities that can be referenced across threads. Add an item:

```bash
curl -X POST http://localhost:8000/api/v1/shared_cache -d '{"key": "fact", "value": "42", "thread_id": "<id>"}' -H 'Content-Type: application/json'
```

View cache entries visible to a thread:

```bash
curl http://localhost:8000/api/v1/shared_cache?thread_id=<id>
```

Import an existing cache entry into a thread (adds the thread tag):

```bash
curl -X POST http://localhost:8000/api/v1/shared_cache/import -d '{"key": "fact", "thread_id": "<other>"}' -H 'Content-Type: application/json'
```
