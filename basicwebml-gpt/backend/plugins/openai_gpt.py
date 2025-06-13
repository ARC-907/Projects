import os
import openai

class Plugin:
    """Plugin that forwards prompts to the OpenAI API."""

    def get_metadata(self):
        return {"name": "openai_gpt", "description": "OpenAI completion", "type": "remote"}

    def predict(self, prompt: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        openai.api_key = api_key
        resp = openai.Completion.create(model="text-davinci-003", prompt=prompt, max_tokens=50)
        return resp.choices[0].text.strip()
