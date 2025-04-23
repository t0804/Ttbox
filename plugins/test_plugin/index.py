from core.plugin import BasePlugin
from core import config
from PyQt6.QtGui import QIcon
from .ui import Main_window
import os

class TestPlugin(BasePlugin):
    def name(self):
        return 'test_plugin'

    def icon(self):
        icon_path = os.path.join(config.ICONS_DIR, 'test_plugin_icon.svg')
        return QIcon(str(icon_path))

    def version(self) -> str:
        return '1.0.0'

    def create_window(self):

        return Main_window()

