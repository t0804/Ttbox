from core.plugin import BasePlugin
from .main_window import RegexTesterMainWindow


class RegexTesterPlugin(BasePlugin):
    @property
    def name(self):
        return '正则测试器'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = RegexTesterMainWindow()
        self._window.show()
