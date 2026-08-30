from core.plugin import BasePlugin
from .main_window import QRGeneratorMainWindow


class QRGeneratorPlugin(BasePlugin):
    @property
    def name(self):
        return '二维码生成'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = QRGeneratorMainWindow()
        self._window.show()
