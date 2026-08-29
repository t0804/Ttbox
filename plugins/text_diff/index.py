from core.plugin import BasePlugin
from .main_window import TextDiffMainWindow


class TextDiffPlugin(BasePlugin):
    @property
    def name(self):
        return '文本对比'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = TextDiffMainWindow()
        self._window.show()
