from core.plugin import BasePlugin
from .main_window import Base64UrlMainWindow


class Base64UrlPlugin(BasePlugin):
    @property
    def name(self):
        return 'Base64/URL编解码'

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        self._window = Base64UrlMainWindow()
        self._window.show()
