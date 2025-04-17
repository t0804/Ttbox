import os
import importlib
from typing import Callable
from main_window_ui import MainWindowUI


class MainWindowLogic:
    """处理主窗口的业务逻辑，与UI解耦"""

    def __init__(self, ui: MainWindowUI):
        self.ui = ui
        # self.plugins = {}
        # self.load_plugins()


    def load_plugins(self):
        """动态加载所有插件"""
        plugin_dir = "../plugins"
        for plugin_name in os.listdir(plugin_dir):
            if not os.path.isdir(os.path.join(plugin_dir, plugin_name)):
                continue

            try:
                module = importlib.import_module(f"plugins.{plugin_name}.ui")
                btn = self.ui.add_plugin_button(module.PLUGIN_NAME)
                btn.clicked.connect(self.make_plugin_opener(module))
                self.plugins[plugin_name] = module
            except ImportError as e:
                print(f"加载插件失败: {plugin_name}\nError: {e}")

    def make_plugin_opener(self, module) -> Callable:
        """生成插件打开函数的闭包"""

        def open_plugin():
            plugin_window = module.PluginWindow()
            plugin_window.exec()

        return open_plugin