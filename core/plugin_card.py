# 插件卡片
from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from core import logger
logger = logger.get_logger(__name__)

# 每个卡片应该是一个对象
class PluginCard(QFrame):
    # 点击信号
    card_clicked = pyqtSignal(object)

    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin
        self.create_card()

    def create_card(self):

        self.setFixedSize(180, 120)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QLabel()
        pixmap = QPixmap(self.plugin.icon().pixmap(QSize(48, 48)))

        # pixmap = QPixmap('./plugin_default_icon.svg')
        icon.setPixmap(pixmap.scaled(QSize(48, 48)))
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(self.plugin.name)
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            logger.debug(f'点击了插件卡片: {self.plugin.name}')
            self.card_clicked.emit(self.plugin)
            # self.plugin.create_window()
