import os
import json
import uuid
import datetime
from typing import List, Dict, Any, Set

THREADS_DIR = os.path.join(os.path.dirname(__file__), "threads")
os.makedirs(THREADS_DIR, exist_ok=True)
CACHE_FILE = os.path.join(os.path.dirname(__file__), "shared_cache.json")


class ThreadSession:
    """Represents a conversation thread."""

    def __init__(self, name: str, thread_id: str | None = None):
        self.thread_id = thread_id or str(uuid.uuid4())
        self.name = name
        self.messages: List[Dict[str, Any]] = []
        self.local_cache: Dict[str, Any] = {}
        self.created_at = datetime.datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "thread_id": self.thread_id,
            "name": self.name,
            "messages": self.messages,
            "local_cache": self.local_cache,
            "created_at": self.created_at,
        }

    @classmethod
    def from_file(cls, path: str) -> "ThreadSession":
        with open(path, "r") as f:
            data = json.load(f)
        obj = cls(data.get("name", ""), data.get("thread_id"))
        obj.messages = data.get("messages", [])
        obj.local_cache = data.get("local_cache", {})
        obj.created_at = data.get("created_at", datetime.datetime.now().isoformat())
        return obj

    def _path(self) -> str:
        return os.path.join(THREADS_DIR, f"{self.thread_id}.json")

    def save(self) -> None:
        with open(self._path(), "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def delete(self) -> None:
        path = self._path()
        if os.path.exists(path):
            os.remove(path)


class SharedCache:
    """Shared cache with per-thread tagging."""

    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}
        if os.path.isfile(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    self.data = json.load(f) or {}
            except json.JSONDecodeError:
                self.data = {}

    def save(self) -> None:
        with open(CACHE_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def add(self, key: str, value: Any, thread_id: str, tags: Set[str] | None = None) -> None:
        tags = set(tags or [])
        entry = self.data.get(key, {"value": value, "origin_threads": set(), "tags": set(), "timestamp": datetime.datetime.now().isoformat()})
        entry["value"] = value
        entry["origin_threads"] = set(entry.get("origin_threads", [])) | {thread_id}
        entry["tags"] = set(entry.get("tags", [])) | tags
        entry["timestamp"] = datetime.datetime.now().isoformat()
        # convert sets to list for json
        entry["origin_threads"] = list(entry["origin_threads"])
        entry["tags"] = list(entry["tags"])
        self.data[key] = entry
        self.save()

    def import_for_thread(self, key: str, thread_id: str) -> None:
        if key in self.data:
            tags = set(self.data[key].get("tags", []))
            tags.add(thread_id)
            self.data[key]["tags"] = list(tags)
            self.save()

    def get_for_thread(self, thread_id: str) -> Dict[str, Any]:
        result = {}
        for k, v in self.data.items():
            origins = set(v.get("origin_threads", []))
            tags = set(v.get("tags", []))
            if thread_id in origins or thread_id in tags:
                result[k] = v
        return result
