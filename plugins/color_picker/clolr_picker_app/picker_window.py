from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QPixmap
import mss
from pynput import mouse, keyboard


class PickerWindow(QWidget):
    """全屏取色窗口 - 基础UI版本"""

    def __init__(self):
        super().__init__()
        self.setup_variables()
        self.setup_ui()
        self.setup_window_properties()


    def setup_window_properties(self):
        """设置窗口属性"""
        # 全屏、无边框、置顶、透明背景
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
            # Qt.Tool
        )
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.showFullScreen()  # 全屏显示


        # 🔴 关键修复1：强制窗口获取焦点（光标生效的核心前提）
        self.activateWindow()  # 激活窗口，提升窗口优先级
        self.setFocus(Qt.MouseFocusReason)  # 强制获取鼠标焦点

        # 🔴 关键修复2：捕获鼠标（确保窗口独占鼠标事件，光标样式100%生效）
        self.grabMouse()

        # 🔴 关键优化：替换为专业吸管光标（替代错误的Qt.BusyCursor）
        # 三选一，推荐Qt.CrossCursor（十字准星）+ 后续自定义吸管图标，兼顾通用和专业
        self.setCursor(Qt.CrossCursor)  # 方案1：系统十字准星（最通用，无兼容问题）
        # self.setCursor(Qt.WhatsThisCursor)  # 方案2：系统吸管光标（部分系统显示为问号，兼容稍弱）
        # self.setCursor(Qt.PointingHandCursor)  # 方案3：手型光标（备用）

    def setup_variables(self):
        """初始化变量"""
        self.is_picking = True  # 是否正在取色
        self.current_pos = QPoint(0, 0)  # 当前鼠标位置
        self.current_color = QColor("#FFFFFF")  # 当前颜色
        self.magnifier_size = 200  # 放大镜尺寸
        self.zoom_factor = 8  # 放大倍数

        # 定时器用于更新鼠标位置
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_mouse_position)
        self.update_timer.start(16)  # ~60fps

    def setup_ui(self):
        """设置UI组件"""
        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # 顶部信息栏
        self.info_label = QLabel("点击选择颜色 • ESC取消")
        self.info_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 150);
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.info_label.setAlignment(Qt.AlignCenter)

        # 放大镜容器（自定义绘制）
        # self.magnifier_container = QWidget()
        # self.magnifier_container.setFixedSize(self.magnifier_size, self.magnifier_size)

        # 颜色信息显示
        color_info_layout = QHBoxLayout()

        # 颜色预览块
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(40, 40)
        self.color_preview.setStyleSheet("background-color: #FF0000; border: 2px solid white;")

        # 颜色数值
        self.color_value_label = QLabel("#FFFFFF")
        self.color_value_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # 坐标显示
        self.position_label = QLabel("(0, 0)")
        self.position_label.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                font-size: 14px;
            }
        """)

        color_info_layout.addWidget(self.color_preview)
        color_info_layout.addWidget(self.color_value_label)
        color_info_layout.addStretch()
        color_info_layout.addWidget(self.position_label)

        # 添加到布局
        layout.addWidget(self.info_label, 0, Qt.AlignTop | Qt.AlignCenter)
        layout.addStretch()
        # layout.addWidget(self.magnifier_container, 0, Qt.AlignCenter)
        layout.addLayout(color_info_layout)
        layout.addStretch()

    def update_mouse_position(self):
        """更新鼠标位置和颜色"""
        if not self.is_picking:
            return

        # 获取全局鼠标位置
        cursor_pos = self.cursor().pos()
        self.current_pos = cursor_pos

        # 更新坐标显示
        self.position_label.setText(f"({cursor_pos.x()}, {cursor_pos.y()})")

        # 获取颜色并更新显示
        color = self.get_color_at_position(cursor_pos.x(), cursor_pos.y())
        if color:
            self.current_color = color
            self.update_color_display()

        # 触发重绘（绘制放大镜）
        # self.magnifier_container.update()

    def get_color_at_position(self, x, y):
        """获取指定位置的颜色"""
        try:
            with mss.mss() as sct:
                monitor = {"top": y, "left": x, "width": 1, "height": 1}
                screenshot = sct.grab(monitor)
                pixel = screenshot.pixel(0, 0)
                # 根据你的测试结果调整顺序
                return QColor(pixel[0], pixel[1], pixel[2])
        except:
            return None

    def update_color_display(self):
        """更新颜色显示"""
        hex_color = self.current_color.name()
        self.color_preview.setStyleSheet(f"""
            background-color: {hex_color};
            border: 2px solid white;
            border-radius: 3px;
        """)
        self.color_value_label.setText(hex_color)


    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.button() == Qt.LeftButton and self.is_picking:
            self.is_picking = False
            self.close()  # 关闭取色窗口
            # 这里应该发射信号，稍后添加
            print(f"选中颜色: {self.current_color.name()}")
        super().mousePressEvent(event)

    def keyPressEvent(self, event):
        """键盘事件"""
        if event.key() == Qt.Key_Escape and self.is_picking:
            self.is_picking = False
            self.close()
            print("取色取消")
        super().keyPressEvent(event)
    def focusOutEvent(self, event):
        """窗口失焦：自动取消取色（如点击其他窗口）"""
        self.pick_canceled.emit()
        self._release_resources()
        self.close()
        super().focusOutEvent(event)

    def closeEvent(self, event):
        """窗口关闭时：兜底释放资源"""
        self._release_resources()
        event.accept()
import sys
from PySide6.QtWidgets import QApplication


app = QApplication(sys.argv)
window = PickerWindow()
sys.exit(app.exec())