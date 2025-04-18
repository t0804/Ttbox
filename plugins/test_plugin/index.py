from core.plugin import BasePlugin
from PyQt6.QtGui import QIcon
from .ui import Main_window

class TestPlugin(BasePlugin):
    def name(self):
        return 'test_plugin'

    def icon(self):
        return QIcon('./icon.svg')

    def version(self) -> str:
        return '1.0.0'

    def create_window(self):

        return Main_window()

