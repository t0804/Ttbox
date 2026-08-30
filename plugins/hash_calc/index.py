from core.plugin import BasePlugin
from .main_window import HashCalcMainWindow


class HashCalcPlugin(BasePlugin):
    @property
    def name(self):
        return '哈希计算'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = HashCalcMainWindow()
        self._window.show()
