import os
from PySide6.QtGui import QIcon
from core.plugin import BasePlugin
from .clolr_picker_app.main_window import ColorPickerMainWindow

class ColorPickerPlugin(BasePlugin):
    @property
    def name(self):
        return '颜色选择器'
    @property
    def version(self) -> str:
        return '1.0.0'

    def icon(self):
        # 插件图标路径
        icon_path = os.path.join(os.path.dirname(__file__), "color_picker.svg")
        return QIcon(icon_path)
    def create_window(self):

        self.main_window = ColorPickerMainWindow()
        self.main_window.show()
