export async function generate(prompt, model) {
  const res = await fetch('/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, prompt })
  });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function listPlugins() {
  const res = await fetch('/api/v1/plugins');
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function refreshPlugins() {
  const res = await fetch('/api/v1/plugins/refresh', { method: 'POST' });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function listThreads() {
  const res = await fetch('/api/v1/threads');
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function createThread(name) {
  const res = await fetch('/api/v1/threads', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function sendMessage(threadId, prompt, model) {
  const res = await fetch(`/api/v1/threads/${threadId}/messages`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model, prompt })
  });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function getSharedCache(threadId) {
  const res = await fetch(`/api/v1/shared_cache?thread_id=${threadId}`);
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function importCache(key, threadId) {
  const res = await fetch('/api/v1/shared_cache/import', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key, thread_id: threadId })
  });
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}

export async function getThread(threadId) {
  const res = await fetch(`/api/v1/threads/${threadId}`);
  if (!res.ok) throw new Error('Request failed');
  return res.json();
}
