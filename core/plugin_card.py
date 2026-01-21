# 插件卡片
from PyQt6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize

# 每个卡片应该是一个对象
class PluginCard(QFrame):
    def __init__(self, plugin):
        super().__init__()
        self.plugin = plugin

    def create_card(self):
        card = QFrame()
        card.setFixedSize(180, 120)
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon = QLabel()
        pixmap = QPixmap(self.plugin.icon().pixmap(QSize(48, 48)))

        # pixmap = QPixmap('./plugin_default_icon.svg')
        icon.setPixmap(pixmap.scaled(QSize(48, 48)))
        layout.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(self.plugin.name())
        title_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        return card