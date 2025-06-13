from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .gpt_engine import MLMatrix

app = FastAPI(title="BasicWebML-GPT", version="0.2.0")


@app.get("/health")
async def health():
    return {"status": "ok"}

ml_matrix = MLMatrix()


class GenerateRequest(BaseModel):
    model: str
    prompt: str


class GenerateResponse(BaseModel):
    response: str


@app.post("/api/v1/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    try:
        result = ml_matrix.predict(req.model, req.prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return GenerateResponse(response=result)


@app.get("/api/v1/plugins")
async def list_plugins():
    return {"plugins": ml_matrix.list_plugins()}


@app.post("/api/v1/plugins/refresh")
async def refresh_plugins():
    return {"plugins": ml_matrix.reload_plugins()}

from .models import ThreadSession, SharedCache, THREADS_DIR
import os
import json
from typing import List

# Load existing threads
threads = {}
for fname in os.listdir(THREADS_DIR):
    if fname.endswith('.json'):
        path = os.path.join(THREADS_DIR, fname)
        t = ThreadSession.from_file(path)
        threads[t.thread_id] = t

shared_cache = SharedCache()


class ThreadCreateRequest(BaseModel):
    name: str


class ThreadInfo(BaseModel):
    thread_id: str
    name: str


class MessageRequest(BaseModel):
    model: str
    prompt: str


class MessageResponse(BaseModel):
    response: str
    thread_id: str


@app.get("/api/v1/threads", response_model=List[ThreadInfo])
async def list_threads():
    return [ThreadInfo(thread_id=t.thread_id, name=t.name) for t in threads.values()]


@app.post("/api/v1/threads", response_model=ThreadInfo)
async def create_thread(req: ThreadCreateRequest):
    t = ThreadSession(req.name)
    threads[t.thread_id] = t
    t.save()
    return ThreadInfo(thread_id=t.thread_id, name=t.name)


@app.put("/api/v1/threads/{thread_id}", response_model=ThreadInfo)
async def rename_thread(thread_id: str, req: ThreadCreateRequest):
    thread = threads.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    thread.name = req.name
    thread.save()
    return ThreadInfo(thread_id=thread_id, name=thread.name)


@app.delete("/api/v1/threads/{thread_id}")
async def delete_thread(thread_id: str):
    thread = threads.pop(thread_id, None)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    thread.delete()
    return {"status": "deleted"}


@app.get("/api/v1/threads/{thread_id}")
async def get_thread(thread_id: str):
    thread = threads.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread.to_dict()


@app.get("/api/v1/threads/{thread_id}/archive")
async def get_thread_archive(thread_id: str):
    thread = threads.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread.to_dict()


@app.post("/api/v1/threads/{thread_id}/messages", response_model=MessageResponse)
async def send_message(thread_id: str, req: MessageRequest):
    thread = threads.get(thread_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    try:
        resp_text = ml_matrix.predict(req.model, req.prompt)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    thread.messages.append({"prompt": req.prompt, "response": resp_text})
    thread.save()
    return MessageResponse(response=resp_text, thread_id=thread_id)


class CacheAddRequest(BaseModel):
    key: str
    value: str
    thread_id: str
    tags: List[str] | None = None


@app.get("/api/v1/shared_cache")
async def get_shared_cache(thread_id: str):
    return shared_cache.get_for_thread(thread_id)


@app.post("/api/v1/shared_cache")
async def add_shared_cache(req: CacheAddRequest):
    shared_cache.add(req.key, req.value, req.thread_id, set(req.tags or []))
    return {"status": "ok"}


class CacheImportRequest(BaseModel):
    key: str
    thread_id: str


@app.post("/api/v1/shared_cache/import")
async def import_shared_cache(req: CacheImportRequest):
    shared_cache.import_for_thread(req.key, req.thread_id)
    return {"status": "ok"}

