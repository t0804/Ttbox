from PySide6.QtCore import QEventLoop, QTimer
from .picker_window import PickerWindow
from core.logger import get_logger

logger = get_logger(__name__)


def start_screen_color_pick():
    """启动全屏取色，返回选中的QColor（无效=取消）"""
    picker = PickerWindow()
    loop = QEventLoop()

    # 延迟 quit 防止在事件处理中途退出事件循环
    picker.finished.connect(lambda: QTimer.singleShot(0, loop.quit))

    loop.exec()

    result = picker.selected_color
    logger.debug(f"取色完成: isValid={result.isValid()}, value={result.name()}")
    return result
