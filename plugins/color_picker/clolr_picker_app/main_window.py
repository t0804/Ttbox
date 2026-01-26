from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
                               QPushButton, QLabel, QSlider, QLineEdit)
from PySide6.QtCore import Qt


class ColorPickerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("颜色选择器")
        self.setGeometry(100, 100, 300, 200)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 上半区左右布局
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        top_layout.addWidget(self.create_color_display())
        top_layout.addLayout(self.create_right_layout())

        self.buttons = self.create_buttons()
        main_layout.addWidget(self.buttons)


    def create_color_display(self):
        color_label = QLabel()
        # color_label.setMinimumSize(100,50)
        color_label.setFixedSize(100,50)
        color_label.setStyleSheet("background-color: #FF0000; border: 2px solid black;")
        return color_label

    def create_right_layout(self):
        right_layout = QVBoxLayout()

        # 先创建上半部分的标签和输入框
        color_value_layout = QVBoxLayout()
        # hex
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("HEX:"))
        hex_input = QLineEdit()
        hex_input.setFixedWidth(100)
        hex_layout.addWidget(hex_input)
        hex_layout.addWidget(QPushButton("复制"))
        color_value_layout.addLayout(hex_layout)
        # RGB
        rgb_layout = QHBoxLayout()
        rgb_layout.addWidget(QLabel("RGB:"))
        rgb_input = QLineEdit()
        rgb_input.setFixedWidth(100)
        rgb_layout.addWidget(rgb_input)
        rgb_layout.addWidget(QPushButton("复制"))
        color_value_layout.addLayout(rgb_layout)
        # HSL
        hsl_layout = QHBoxLayout()
        hsl_layout.addWidget(QLabel("HSL:"))
        hsl_input = QLineEdit()
        hsl_input.setFixedWidth(100)
        hsl_layout.addWidget(hsl_input)
        hsl_layout.addWidget(QPushButton("复制"))
        color_value_layout.addLayout(hsl_layout)

        right_layout.addLayout(color_value_layout)

        slider_frame = self.create_sliders()
        right_layout.addWidget(slider_frame)
        return right_layout

    def create_sliders(self):
        slider_frame = QFrame()
        # slider_frame.setStyleSheet("border: 1px solid black;")
        layout = QVBoxLayout(slider_frame)

        # 滑块有默认大小策略，会自适应
        red_slider = QSlider(Qt.Orientation.Horizontal)
        green_slider = QSlider(Qt.Orientation.Horizontal)
        blue_slider = QSlider(Qt.Orientation.Horizontal)
        red_item = QHBoxLayout()
        red_item.addWidget(QLabel("R:"))
        red_text = QLineEdit()
        red_text.setFixedWidth(35)
        red_item.addWidget(red_text)
        red_item.addStretch()
        layout.addLayout(red_item)
        layout.addWidget(red_slider)
        green_item = QHBoxLayout()
        green_item.addWidget(QLabel("G:"))
        green_text = QLineEdit()
        green_text.setFixedWidth(35)
        green_item.addWidget(green_text)
        green_item.addStretch()
        layout.addLayout(green_item)
        layout.addWidget(green_slider)
        blue_item = QHBoxLayout()
        blue_item.addWidget(QLabel("B:"))
        blue_text = QLineEdit()
        blue_text.setFixedWidth(35)
        blue_item.addWidget(blue_text)
        blue_item.addStretch()
        layout.addLayout(blue_item)
        layout.addWidget(blue_slider)

        return slider_frame

    def create_buttons(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.get_color_button = QPushButton("取色")
        self.reset_button = QPushButton("重置")

        layout.addWidget(self.get_color_button)
        layout.addWidget(self.reset_button)

        return widget
    def resizeEvent(self, event):
        """窗口大小变化时触发"""
        print(f"窗口大小: {self.width()} x {self.height()}")
        if hasattr(self, 'color_display'):
            print(f"颜色显示区: {self.color_display.size()}")
        super().resizeEvent(event)
import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
w = ColorPickerMainWindow()
w.show()

sys.exit(app.exec())
