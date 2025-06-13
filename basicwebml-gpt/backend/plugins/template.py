class Plugin:
    """Template for developing new plugins."""

    def get_metadata(self):
        return {
            "name": "template",
            "description": "Describe plugin",
            "type": "demo",
        }

    def predict(self, prompt: str) -> str:
        # Implement logic here
        return "..."
