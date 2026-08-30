from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, Signal
from core import logger

logger = logger.get_logger(__name__)


class PluginCard(QFrame):
    card_clicked = Signal(object)

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin
        self.setObjectName("plugin_card")
        self.setFixedSize(240, 110)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(12)

        icon = QLabel()
        pixmap = QPixmap(self.plugin.icon().pixmap(QSize(36, 36)))
        icon.setPixmap(pixmap)
        icon.setFixedSize(36, 36)
        layout.addWidget(icon)

        text_col = QVBoxLayout()
        text_col.setSpacing(2)
        name = QLabel(self.plugin.name)
        name.setStyleSheet("font-size: 14px; font-weight: 600; color: #111827;")
        text_col.addWidget(name)

        ver = QLabel(f"v{self.plugin.version}")
        ver.setStyleSheet("font-size: 11px; color: #9CA3AF;")
        text_col.addWidget(ver)
        text_col.addStretch()
        layout.addLayout(text_col, 1)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            logger.debug(f'点击了插件卡片: {self.plugin.name}')
            self.card_clicked.emit(self.plugin)
