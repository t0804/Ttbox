from core.plugin import BasePlugin
from core import config
from PySide6.QtGui import QIcon
from .ui import Main_window
import os

class TestPlugin(BasePlugin):
    @property
    def name(self):
        return 'test_plugin'

    def icon(self):
        icon_path = os.path.join(config.ICONS_DIR, 'test_plugin_icon.svg')
        return QIcon(str(icon_path))

    @property
    def version(self) -> str:
        return '1.0.0'

    def create_window(self):
        print('创建一个新窗口')
        self.window = Main_window()
        self.window.show()
        return self.window

