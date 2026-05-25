import os
from core.plugin import BasePlugin
from PySide6.QtGui import QIcon
from .main_window import TimestampConverterMainWindow

class TimestampConverterPlugin(BasePlugin):
    @property
    def name(self):
        return '时间戳转换'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = TimestampConverterMainWindow()

    def icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), 'timestamp_converter.svg')
        return QIcon(icon_path)
