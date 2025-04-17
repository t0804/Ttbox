import sys
from PyQt6.QtWidgets import QApplication
from main_window_ui import MainWindowUI
from main_window_logic import MainWindowLogic


def run():
    app = QApplication(sys.argv)

    # 加载样式
    with open("./style.qss", "r", encoding='utf8') as f:
        app.setStyleSheet(f.read())

    # 初始化UI和逻辑
    ui = MainWindowUI()
    # logic = MainWindowLogic(ui)  # 将UI实例注入逻辑层

    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()