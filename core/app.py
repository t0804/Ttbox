import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from core.main_window_ui import MainWindowUI
from core.config import BASE_DIR
from core import logger

logger = logger.get_logger(__name__)


def run():
    logger.debug('run app')
    app = QApplication(sys.argv)

    qss_path = BASE_DIR / "core" / "style.qss"
    if qss_path.exists():
        app.setStyleSheet(qss_path.read_text(encoding="utf-8"))

    ui = MainWindowUI()
    ui.show()
    sys.exit(app.exec())
