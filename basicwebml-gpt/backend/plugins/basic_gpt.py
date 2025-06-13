class Plugin:
    """A simple echo model plugin for demonstration."""

    def get_metadata(self):
        return {"name": "basic_gpt", "description": "Echo plugin", "type": "demo"}

    def predict(self, prompt: str) -> str:
        return f"Echo: {prompt}"
