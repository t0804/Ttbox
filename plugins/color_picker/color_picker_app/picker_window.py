import mss
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QCursor, QPixmap, QImage
from core.logger import get_logger

logger = get_logger(__name__)


class PickerWindow(QWidget):
    """全屏取色窗口，以冻结截图作背景，自绘放大镜和信息面板"""

    finished = Signal()

    def __init__(self):
        super().__init__()
        self.selected_color = QColor()
        self._pick_done = False
        self.current_color = QColor(0, 0, 0)
        self.cursor_pos = QCursor.pos()

        self.capture_radius = 8
        self.zoom_factor = 10
        self.grid_size = 17
        self.magnifier_size = 170

        self.pixel_grid = [[(0, 0, 0)] * self.grid_size for _ in range(self.grid_size)]

        self.screenshot = None
        self.background = QPixmap()
        self.capture_background()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.setCursor(Qt.CrossCursor)

        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(33)

    def capture_background(self):
        """截取全屏作为静态背景"""
        try:
            with mss.mss() as sct:
                self.screenshot = sct.grab(sct.monitors[1])
                img = QImage(
                    self.screenshot.bgra,
                    self.screenshot.width,
                    self.screenshot.height,
                    QImage.Format.Format_ARGB32,
                )
                self.background = QPixmap.fromImage(img)
        except Exception as e:
            logger.error(f"截图失败: {e}")

    def on_timer(self):
        """定时器回调：更新光标位置和像素网格"""
        if not self.screenshot:
            return

        self.cursor_pos = QCursor.pos()
        cx, cy = self.cursor_pos.x(), self.cursor_pos.y()
        r = self.capture_radius

        try:
            for dy in range(-r, r + 1):
                row_idx = dy + r
                for dx in range(-r, r + 1):
                    px, py = cx + dx, cy + dy
                    if 0 <= px < self.screenshot.width and 0 <= py < self.screenshot.height:
                        p = self.screenshot.pixel(px, py)
                        self.pixel_grid[row_idx][dx + r] = (p[0], p[1], p[2])
                    else:
                        self.pixel_grid[row_idx][dx + r] = (0, 0, 0)

            cp = self.pixel_grid[r][r]
            self.current_color = QColor(cp[0], cp[1], cp[2])
        except Exception as e:
            logger.error(f"取色失败: {e}")

        self.update()

    def paintEvent(self, event):
        """绘制背景截图 + 放大镜 + 信息面板"""
        painter = QPainter(self)

        if not self.background.isNull():
            painter.drawPixmap(0, 0, self.background)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        sx, sy = self.magnifier_position()
        self.draw_magnifier(painter, sx, sy)
        self.draw_info_panel(painter, sx, sy)

    def magnifier_position(self):
        """计算放大镜左上角位置（带屏幕边缘检测）"""
        mg = self.magnifier_size
        cx, cy = self.cursor_pos.x(), self.cursor_pos.y()
        gap = 20

        x = cx + gap
        y = cy - mg - gap

        sw = self.screenshot.width if self.screenshot else 1920
        sh = self.screenshot.height if self.screenshot else 1080

        if y < 0:
            y = cy + gap
        if x + mg > sw:
            x = cx - mg - gap
        if y + mg > sh:
            y = sh - mg - gap
        if x < 0:
            x = gap

        return int(x), int(y)

    def draw_magnifier(self, painter, sx, sy):
        """绘制像素放大镜（网格 + 边框 + 十字准星）"""
        z = self.zoom_factor

        for dy in range(self.grid_size):
            for dx in range(self.grid_size):
                r, g, b = self.pixel_grid[dy][dx]
                painter.fillRect(sx + dx * z, sy + dy * z, z, z, QColor(r, g, b))

        pen = QPen(QColor(255, 255, 255, 60))
        pen.setWidth(1)
        painter.setPen(pen)
        for i in range(self.grid_size + 1):
            painter.drawLine(sx + i * z, sy, sx + i * z, sy + self.magnifier_size)
            painter.drawLine(sx, sy + i * z, sx + self.magnifier_size, sy + i * z)

        pen = QPen(QColor(255, 255, 255, 200))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(sx, sy, self.magnifier_size, self.magnifier_size)

        pen = QPen(QColor(255, 50, 50, 230))
        pen.setWidth(2)
        painter.setPen(pen)
        cx = self.magnifier_size // 2
        cs = z // 2
        painter.drawLine(sx + cx - cs, sy + cx, sx + cx + cs, sy + cx)
        painter.drawLine(sx + cx, sy + cx - cs, sx + cx, sy + cx + cs)

    def draw_info_panel(self, painter, sx, sy):
        """绘制浮动信息面板（HEX、RGB、POS）"""
        pw, ph = 200, 110
        pad = 12

        px = sx
        py = sy + self.magnifier_size + 6

        sh = self.screenshot.height if self.screenshot else 1080
        if py + ph > sh:
            py = sy - ph - 6

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 200))
        painter.drawRoundedRect(px, py, pw, ph, 6, 6)

        swatch = 24
        painter.setPen(QPen(QColor(255, 255, 255, 80), 1))
        painter.setBrush(self.current_color)
        painter.drawRoundedRect(px + pad, py + pad, swatch, swatch, 3, 3)

        painter.setPen(QColor(255, 255, 255))
        font = QFont("Consolas", 12)
        painter.setFont(font)
        painter.drawText(
            px + pad + swatch + pad, py + pad,
            pw - pad * 3 - swatch, swatch,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            self.current_color.name().upper()
        )

        painter.setPen(QColor(180, 180, 180))
        font = QFont("Consolas", 10)
        painter.setFont(font)
        rgb_text = f"RGB({self.current_color.red()}, {self.current_color.green()}, {self.current_color.blue()})"
        painter.drawText(px + pad, py + pad + swatch + 6, pw - pad * 2, 22,
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, rgb_text)

        pos_text = f"POS({self.cursor_pos.x()}, {self.cursor_pos.y()})"
        painter.drawText(px + pad, py + pad + swatch + 26, pw - pad * 2, 22,
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, pos_text)

    def mousePressEvent(self, event):
        """左键按下保存颜色，右键/其他直接取消"""
        if event.button() == Qt.MouseButton.LeftButton:
            logger.debug(f"取色按下: color={self.current_color.name()}")
            self._pick_done = True
            self.selected_color = self.current_color
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """左键释放确认取色，右键释放取消"""
        if event.button() == Qt.MouseButton.LeftButton and self._pick_done:
            logger.debug("取色确认，关闭窗口")
            self.finished.emit()
            QTimer.singleShot(0, self.close)
            event.accept()
        elif event.button() == Qt.MouseButton.RightButton and not self._pick_done:
            logger.debug("右键取消取色")
            self._pick_done = True
            self.selected_color = QColor()
            self.finished.emit()
            QTimer.singleShot(0, self.close)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        """ESC 取消取色"""
        if event.key() == Qt.Key_Escape:
            logger.debug("ESC 取消取色")
            self._pick_done = True
            self.selected_color = QColor()
            self.finished.emit()
            QTimer.singleShot(0, self.close)
        super().keyPressEvent(event)

    def focusOutEvent(self, event):
        """失焦取消（ALT+TAB 等），若已确认取色则忽略"""
        if not self._pick_done:
            logger.debug("失焦取消取色")
            self._pick_done = True
            self.selected_color = QColor()
            self.finished.emit()
            QTimer.singleShot(0, self.close)
        super().focusOutEvent(event)

    def closeEvent(self, event):
        """关闭时停止定时器"""
        self.timer.stop()
        event.accept()
