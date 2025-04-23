# core/plugin_manager.py
import importlib
import os
from typing import List
from .plugin import BasePlugin

def load_plugins() -> List[BasePlugin]:
    """加载所有合规插件"""
    plugins = []
    for plugin_dir in os.listdir("plugins"):
        try:
            module = importlib.import_module(f"plugins.{plugin_dir}")
            plugin_class = getattr(module, "__plugin_class__")
            if issubclass(plugin_class, BasePlugin):
                plugins.append(plugin_class())
        except (ImportError, AttributeError):
            continue
    return plugins