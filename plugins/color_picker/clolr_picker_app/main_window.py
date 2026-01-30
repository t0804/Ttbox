import time

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFrame,
                               QPushButton, QLabel, QSlider, QLineEdit, QColorDialog, QColormap)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from core.logger import get_logger
from uitls import qt_hsl_to_common, common_hsl_to_qt
from screen_color_picker import start_screen_color_pick
logger = get_logger(__name__)



class ColorPickerMainWindow(QMainWindow):
    # 颜色变化信号
    color_changed = Signal(QColor)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("颜色选择器")
        self.setGeometry(100, 100, 300, 200)
        self._current_color = QColor("#000000")
        self.color_label_border_style = "border: 2px solid black;"
        self.updating = False
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
        # 连接信号
        self.color_changed.connect(self.on_color_label_changed)

    def on_color_label_changed(self, color):
        if self.updating:
            return
        self.updating = True

        try:
            self._current_color = color
            self.hex_input.setText(color.name())
            self.rgb_input.setText(f"{color.red()},{color.green()},{color.blue()}")
            h_qt = color.hue()
            s_qt = color.saturation()
            l_qt = color.lightness()
            # Qt HSL → 通用HSL
            h_common, s_common, l_common = qt_hsl_to_common(h_qt, s_qt, l_qt)
            # 显示为「色相,饱和度%,亮度%」（符合用户习惯）
            self.hsl_input.setText(f"{h_common},{s_common}%,{l_common}%")

            # 更新滑块和输入框
            self.red_slider.setValue(color.red())
            self.green_slider.setValue(color.green())
            self.blue_slider.setValue(color.blue())
            self.red_text.setText(str(color.red()))
            self.green_text.setText(str(color.green()))
            self.blue_text.setText(str(color.blue()))
            # 更新颜色
            self.color_label.setStyleSheet(
                f"background-color: {color.name()}; {self.color_label_border_style}"
            )


        except Exception as e:
            logger.error(f"更新颜色显示时出错: {e}")

        self.updating = False


    def create_color_display(self):
        self.color_label = QLabel()
        # color_label.setMinimumSize(100,50)
        self.color_label.setFixedSize(100,50)
        self.color_label.setStyleSheet(f"background-color:{self._current_color.name()}; {self.color_label_border_style}")
        # 点击事件
        self.color_label.mousePressEvent = self.on_color_label_click
        return self.color_label

    def on_color_label_click(self, event):
        if event.button() == Qt.LeftButton:

            color_dialog = QColorDialog(self._current_color)
            color_dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
            color_dialog.exec()

            color = color_dialog.selectedColor()
            # 用户点击取消后返回的QColor对象是无效的
            if color.isValid():
                self._current_color = color
                self.color_label.setStyleSheet(
                    f"background-color: {color.name()}; {self.color_label_border_style}"
                )
                self.color_changed.emit(color)

    def create_right_layout(self):
        right_layout = QVBoxLayout()

        # 先创建上半部分的标签和输入框
        color_value_layout = QVBoxLayout()
        # hex
        hex_layout = QHBoxLayout()
        hex_layout.addWidget(QLabel("HEX:"))
        self.hex_input = QLineEdit()
        self.hex_input.setFixedWidth(120)
        self.hex_input.editingFinished.connect(self.on_hex_input_changed)
        hex_layout.addWidget(self.hex_input)
        hex_copy_button = QPushButton("复制")
        hex_copy_button.clicked.connect(self.on_hex_copy_click)
        hex_layout.addWidget(hex_copy_button)
        color_value_layout.addLayout(hex_layout)
        # RGB
        rgb_layout = QHBoxLayout()
        rgb_layout.addWidget(QLabel("RGB:"))
        self.rgb_input = QLineEdit()
        self.rgb_input.setFixedWidth(120)
        self.rgb_input.editingFinished.connect(self.on_rgb_input_changed)
        rgb_layout.addWidget(self.rgb_input)
        rbg_copy_button = QPushButton("复制")
        rbg_copy_button.clicked.connect(self.on_rgb_copy_click)
        rgb_layout.addWidget(rbg_copy_button)
        color_value_layout.addLayout(rgb_layout)
        # HSL
        hsl_layout = QHBoxLayout()
        hsl_layout.addWidget(QLabel("HSL:"))
        self.hsl_input = QLineEdit()
        self.hsl_input.setFixedWidth(120)
        self.hsl_input.editingFinished.connect(self.on_hsl_input_changed)
        hsl_layout.addWidget(self.hsl_input)
        hsl_copy_button = QPushButton("复制")
        hsl_copy_button.clicked.connect(self.on_hsl_copy_click)
        hsl_layout.addWidget(hsl_copy_button)
        color_value_layout.addLayout(hsl_layout)
        right_layout.addLayout(color_value_layout)

        slider_frame = self.create_sliders()
        right_layout.addWidget(slider_frame)
        # 创建组件后先更新一次颜色显示
        # 因为连接信号在setup_ui最后 现在还没连接无法使用发信号方式初始化，可以放到__init__中setup_ui()前实现
        # self.color_changed.emit(self._current_color)
        self.on_color_label_changed(self._current_color)
        return right_layout

    def on_hex_input_changed(self):
        if self.updating:
            return
        self.updating = True
        try:
            text = self.hex_input.text().strip()
            # 兼容带#和不带#
            if not text.startswith('#'):
                text = '#' + text
            color = QColor(text)
            if color.isValid():
                self._current_color = color
                self.updating = False
                self.color_changed.emit(color)
            else:
                logger.error(f"无效的HEX颜色值: {text}")
                self.updating = False
                self.color_changed.emit(self._current_color)
        except ValueError:
            pass
        self.updating = False

    def on_rgb_input_changed(self):
        if self.updating:
            return
        self.updating = True
        text = self.rgb_input.text().strip()
        try:
            rgb_values = text.split(',')
            if len(rgb_values) == 3:
                red = int(rgb_values[0].strip())
                green = int(rgb_values[1].strip())
                blue = int(rgb_values[2].strip())
                color = QColor(red, green, blue)
                if color.isValid():
                    self._current_color = color
                    self.updating = False
                    self.color_changed.emit(color)
                else:
                    logger.error(f"无效的RGB颜色值: {text}")
                    self.updating = False
                    self.color_changed.emit(self._current_color)
            else:
                logger.error(f"无效的RGB颜色值: {text}")
                self.updating = False
                self.color_changed.emit(self._current_color)
        except Exception as e:
            logger.error(f"RGB值格式错误: {text}, 错误信息: {e}")
            self.updating = False
            self.color_changed.emit(self._current_color)
        self.updating = False

    def on_hsl_input_changed(self):
        if self.updating:
            return
        self.updating = True
        text = self.hsl_input.text().strip()
        try:
            hsl_values = text.split(',')
            if len(hsl_values) == 3:
                # 解析用户输入的通用HSL（支持带%和不带%）
                h = float(hsl_values[0].strip())
                s = float(hsl_values[1].strip().replace('%', ''))  # 去掉%
                l = float(hsl_values[2].strip().replace('%', ''))  # 去掉%

                # 通用HSL → Qt HSL
                h_qt, s_qt, l_qt = common_hsl_to_qt(h, s, l)
                # 创建Qt颜色对象
                color = QColor.fromHsl(h_qt, s_qt, l_qt)

                if color.isValid():
                    self._current_color = color
                    self.updating = False
                    self.color_changed.emit(color)
                else:
                    logger.error(f"无效的HSL颜色值: {text}")
                    self.updating = False
                    self.color_changed.emit(self._current_color)
            else:
                logger.error(f"无效的RGB颜色值: {text}")
                self.updating = False
                self.color_changed.emit(self._current_color)
        except Exception as e:
            logger.error(f"HSL值格式错误: {text}, 错误信息: {e}")
            self.updating = False
            self.color_changed.emit(self._current_color)
        self.updating = False

    def on_hex_copy_click(self):
        QApplication.clipboard().setText(self.hex_input.text())

    def on_rgb_copy_click(self):
        QApplication.clipboard().setText(self.rgb_input.text())

    def on_hsl_copy_click(self):
        QApplication.clipboard().setText(self.hsl_input.text())

    def create_sliders(self):
        slider_frame = QFrame()
        # slider_frame.setStyleSheet("border: 1px solid black;")
        layout = QVBoxLayout(slider_frame)

        # 滑块有默认大小策略，会自适应
        self.red_slider = QSlider(Qt.Orientation.Horizontal)
        self.red_slider.setRange(0, 255)
        self.red_slider.setTickPosition(QSlider.TicksBelow)
        self.red_slider.setTickInterval(50)
        self.red_slider.valueChanged.connect(self.on_red_slider_changed)
        self.green_slider = QSlider(Qt.Orientation.Horizontal)
        self.green_slider.setRange(0, 255)
        self.green_slider.setTickPosition(QSlider.TicksBelow)
        self.green_slider.setTickInterval(50)
        self.green_slider.valueChanged.connect(self.on_green_slider_changed)
        self.blue_slider = QSlider(Qt.Orientation.Horizontal)
        self.blue_slider.setRange(0, 255)
        self.blue_slider.setTickPosition(QSlider.TicksBelow)
        self.blue_slider.setTickInterval(50)
        self.blue_slider.valueChanged.connect(self.on_blue_slider_changed)

        red_item = QHBoxLayout()
        red_item.addWidget(QLabel("R:"))
        self.red_text = QLineEdit()
        self.red_text.setFixedWidth(35)
        self.red_text.textChanged.connect(self.on_red_text_changed)
        red_item.addWidget(self.red_text)
        red_item.addStretch()
        layout.addLayout(red_item)
        layout.addWidget(self.red_slider)
        green_item = QHBoxLayout()
        green_item.addWidget(QLabel("G:"))
        self.green_text = QLineEdit()
        self.green_text.setFixedWidth(35)
        self.green_text.textChanged.connect(self.on_green_text_changed)
        green_item.addWidget(self.green_text)
        green_item.addStretch()
        layout.addLayout(green_item)
        layout.addWidget(self.green_slider)
        blue_item = QHBoxLayout()
        blue_item.addWidget(QLabel("B:"))
        self.blue_text = QLineEdit()
        self.blue_text.setFixedWidth(35)
        self.blue_text.textChanged.connect(self.on_blue_text_changed)
        blue_item.addWidget(self.blue_text)
        blue_item.addStretch()
        layout.addLayout(blue_item)
        layout.addWidget(self.blue_slider)

        return slider_frame

    def on_red_slider_changed(self, value):
        if self.updating:
            return
        self.updating = True
        color = QColor(value, self._current_color.green(), self._current_color.blue())
        self._current_color = color
        # 这里需要先更新标记在发射信号，否则会导致色块不更新
        self.updating = False
        self.color_changed.emit(color)


    def on_green_slider_changed(self, value):
        if self.updating:
            return
        self.updating = True
        color = QColor(self._current_color.red(), value, self._current_color.blue())
        self._current_color = color
        self.updating = False
        self.color_changed.emit(color)

    def on_blue_slider_changed(self, value):
        if self.updating:
            return
        self.updating = True
        color = QColor(self._current_color.red(), self._current_color.green(), value)
        self._current_color = color
        self.updating = False
        self.color_changed.emit(color)

    def on_red_text_changed(self, text):
        if self.updating:
            return
        self.updating = True
        red = int(text.strip())
        if red < 0:
            red = 0
        if red > 255:
            red = 255
        color = QColor(red, self._current_color.green(), self._current_color.blue())
        self._current_color = color
        self.updating = False
        self.color_changed.emit(color)

    def on_green_text_changed(self, text):
        if self.updating:
            return
        self.updating = True
        green = int(text.strip())
        if green < 0:
            green = 0
        if green > 255:
            green = 255
        color = QColor(self._current_color.red(), green, self._current_color.blue())
        self._current_color = color
        self.updating = False
        self.color_changed.emit(color)

    def on_blue_text_changed(self, text):
        if self.updating:
            return
        self.updating = True
        blue = int(text.strip())
        if blue < 0:
            blue = 0
        if blue > 255:
            blue = 255
        color = QColor(self._current_color.red(), self._current_color.green(), blue)
        self._current_color = color
        self.updating = False
        self.color_changed.emit(color)

    def create_buttons(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        get_color_button = QPushButton("取色")
        get_color_button.clicked.connect(self.get_color)
        reset_button = QPushButton("重置")
        reset_button.clicked.connect(self.reset_color)
        layout.addWidget(get_color_button)
        layout.addWidget(reset_button)

        return widget

    def reset_color(self):
        self.color_changed.emit(QColor("#000000"))

    def get_color(self):

        self.hide()
        try:
            # 拾取颜色
            color = start_screen_color_pick()

            if color.isValid():  # 用户点击了OK
                self._current_color = color
                # 直接发射信号，让统一机制处理更新
                self.color_changed.emit(color)

        except Exception as e:
            logger.error(f"取色过程中发生错误: {e}")

        finally:
            # 无论成功失败，都必须恢复窗口
            self.show()
            self.raise_()
            self.activateWindow()


import sys
from PySide6.QtWidgets import QApplication

app = QApplication(sys.argv)
w = ColorPickerMainWindow()
w.show()

sys.exit(app.exec())
