from core.plugin import BasePlugin
from .main_window import JsonFormatterMainWindow


class JsonFormatterPlugin(BasePlugin):
    @property
    def name(self):
        return 'JSON格式化'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = JsonFormatterMainWindow()
        self._window.show()
