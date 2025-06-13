import { useState, useEffect } from 'react';
import { listPlugins, listThreads, createThread, sendMessage, getThread, getSharedCache, importCache } from './api';

export default function App() {
  const [input, setInput] = useState('');
  const [model, setModel] = useState('basic_gpt');
  const [models, setModels] = useState(['basic_gpt']);
  const [threads, setThreads] = useState([]);
  const [current, setCurrent] = useState(null);
  const [history, setHistory] = useState([]);
  const [cache, setCache] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    listPlugins().then(data => setModels(Object.keys(data.plugins))).catch(() => {});
    listThreads().then(data => {
      setThreads(data);
      if (data.length) {
        setCurrent(data[0]);
      }
    }).catch(() => {});
  }, []);

  useEffect(() => {
    if (current) {
      getThread(current.thread_id).then(t => setHistory(t.messages)).catch(() => {});
      getSharedCache(current.thread_id).then(setCache).catch(() => {});
    }
  }, [current]);

  async function newThread() {
    const t = await createThread('thread');
    setThreads([...threads, t]);
    setCurrent(t);
  }

  async function handleSubmit() {
    if (!current) return;
    setLoading(true);
    setError('');
    try {
      const res = await sendMessage(current.thread_id, input, model);
      setHistory([...history, { prompt: input, response: res.response }]);
      setInput('');
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto mt-4 p-4">
      <div className="mb-2 flex space-x-2">
        {threads.map(t => (
          <button key={t.thread_id} onClick={() => setCurrent(t)} className={`px-2 py-1 border ${current && current.thread_id === t.thread_id ? 'bg-blue-200' : ''}`}>{t.name}</button>
        ))}
        <button onClick={newThread} className="px-2 py-1 border">+</button>
      </div>
      <select value={model} onChange={e => setModel(e.target.value)} className="mb-2 border p-1 rounded">
        {models.map(m => <option key={m} value={m}>{m}</option>)}
      </select>
      <textarea value={input} onChange={e => setInput(e.target.value)} className="w-full mb-2 border rounded" />
      <button onClick={handleSubmit} className="px-4 py-2 bg-blue-500 text-white rounded" disabled={loading || !current}>Send</button>
      {loading && <div className="mt-2">Loading...</div>}
      {error && <div className="mt-2 text-red-600">{error}</div>}
      <div className="mt-4">
        {history.map((m, i) => (
          <div key={i} className="mb-2">
            <div className="font-semibold">Prompt:</div>
            <pre className="bg-gray-100 p-2 rounded">{m.prompt}</pre>
            <div className="font-semibold">Response:</div>
            <pre className="bg-gray-100 p-2 rounded">{m.response}</pre>
          </div>
        ))}
      </div>
      {current && (
        <div className="mt-4">
          <div className="font-bold">Shared Cache</div>
          <ul>
            {Object.entries(cache).map(([k, v]) => (
              <li key={k} className="border-b py-1 flex justify-between">
                <span>{k}: {v.value}</span>
                <button onClick={() => importCache(k, current.thread_id)} className="text-sm text-blue-600">import</button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
