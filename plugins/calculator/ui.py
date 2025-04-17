from PyQt6.QtWidgets import QDialog

PLUGIN_NAME = "计算器"  # 必须定义插件名称

class PluginWindow(QDialog):
    """子窗口类名必须为PluginWindow"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle(PLUGIN_NAME)
        # ...具体UI实现