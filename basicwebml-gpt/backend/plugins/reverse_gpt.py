class Plugin:
    """Reverse the input prompt"""

    def get_metadata(self):
        return {"name": "reverse_gpt", "description": "Reverse text plugin", "type": "demo"}

    def predict(self, prompt: str) -> str:
        return prompt[::-1]
