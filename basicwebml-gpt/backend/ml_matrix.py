import importlib
import importlib.util
import os
from typing import Dict, Any
import yaml


class MLMatrix:
    """Manage ML model plugins with hot reloading and metadata."""

    def __init__(self, plugins_path: str = None, config_path: str = None):
        self.plugins_path = plugins_path or os.path.join(os.path.dirname(__file__), "plugins")
        self.config_path = config_path or os.path.join(os.path.dirname(__file__), "ml_config.yaml")
        self.plugins: Dict[str, Any] = {}
        self.load_config()
        self.load_plugins()

    def load_config(self) -> None:
        self.enabled_plugins = None
        if os.path.isfile(self.config_path):
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f) or {}
            self.enabled_plugins = set(data.get("enabled_plugins", []))

    def load_plugins(self) -> None:
        self.plugins = {}
        if not os.path.isdir(self.plugins_path):
            return
        for filename in os.listdir(self.plugins_path):
            if filename.endswith(".py") and not filename.startswith("__"):
                name = filename[:-3]
                if self.enabled_plugins is not None and name not in self.enabled_plugins:
                    continue
                spec = importlib.util.spec_from_file_location(name, os.path.join(self.plugins_path, filename))
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    if hasattr(module, "Plugin"):
                        self.plugins[name] = module.Plugin()

    def reload_plugins(self) -> Dict[str, Any]:
        """Reload plugins from disk."""
        self.load_config()
        self.load_plugins()
        return {name: plugin.get_metadata() for name, plugin in self.plugins.items() if hasattr(plugin, "get_metadata")}

    def list_plugins(self) -> Dict[str, Any]:
        return {name: plugin.get_metadata() for name, plugin in self.plugins.items() if hasattr(plugin, "get_metadata")}

    def predict(self, model_name: str, prompt: str) -> str:
        plugin = self.plugins.get(model_name)
        if not plugin:
            raise ValueError("Model plugin not found")
        if not hasattr(plugin, "predict"):
            raise ValueError("Plugin missing predict method")
        return plugin.predict(prompt)

    def health_check(self) -> Dict[str, bool]:
        return {name: hasattr(plugin, "predict") for name, plugin in self.plugins.items()}
