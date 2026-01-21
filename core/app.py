import sys

from PyQt6.QtWidgets import QApplication
from core.main_window_ui import MainWindowUI
# from main_window_logic import MainWindowLogic
from core import logger
logger = logger.get_logger(__name__)

def run():
    logger.debug('run app')
    app = QApplication(sys.argv)


    # # 加载样式
    # with open("./style.qss", "r", encoding='utf8') as f:
    #     app.setStyleSheet(f.read())

    # 初始化UI和逻辑
    ui = MainWindowUI()
    # logic = MainWindowLogic(ui)  # 将UI实例注入逻辑层

    ui.show()
    sys.exit(app.exec())
