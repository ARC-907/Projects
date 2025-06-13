from fastapi.testclient import TestClient
from backend.app import app
import os
import yaml

client = TestClient(app)
base_dir = os.path.dirname(__file__)
plugins_dir = os.path.join(base_dir, "../backend/plugins")
config_file = os.path.join(base_dir, "../backend/ml_config.yaml")


def test_generate_echo():
    resp = client.post('/api/v1/generate', json={'model': 'basic_gpt', 'prompt': 'hi'})
    assert resp.status_code == 200
    assert resp.json()['response'] == 'Echo: hi'


def test_plugin_reload(tmp_path):
    plugin_code = """class Plugin:\n    def get_metadata(self):\n        return {'name': 'tmp_plugin', 'description': 'tmp', 'type': 'demo'}\n    def predict(self, prompt: str) -> str:\n        return 'tmp:' + prompt\n"""
    plugin_file = os.path.join(plugins_dir, 'tmp_plugin.py')
    with open(plugin_file, 'w') as f:
        f.write(plugin_code)
    # update config to include plugin
    cfg = {'enabled_plugins': ['basic_gpt', 'reverse_gpt', 'openai_gpt', 'tmp_plugin']}
    with open(config_file, 'w') as f:
        yaml.safe_dump(cfg, f)
    try:
        resp = client.post('/api/v1/plugins/refresh')
        assert resp.status_code == 200
        plugins = resp.json()['plugins']
        assert 'tmp_plugin' in plugins
    finally:
        os.remove(plugin_file)
        resp = client.post('/api/v1/plugins/refresh')
        assert resp.status_code == 200

def test_thread_create_and_message():
    resp = client.post('/api/v1/threads', json={'name': 'test'})
    assert resp.status_code == 200
    data = resp.json()
    thread_id = data['thread_id']

    # send message
    resp = client.post(f'/api/v1/threads/{thread_id}/messages', json={'model': 'basic_gpt', 'prompt': 'hi'})
    assert resp.status_code == 200
    assert resp.json()['response'].startswith('Echo')

    # fetch archive
    resp = client.get(f'/api/v1/threads/{thread_id}/archive')
    assert resp.status_code == 200
    arch = resp.json()
    assert arch['messages']

    # cleanup
    client.delete(f'/api/v1/threads/{thread_id}')

