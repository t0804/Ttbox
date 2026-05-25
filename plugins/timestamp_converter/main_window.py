import datetime
import zoneinfo
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QApplication, QComboBox, QFrame)
from PySide6.QtCore import Qt, QTimer, QEvent

class TimestampConverterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode = 'Live'  # 状态机模式 Live or Manual
        self.tbar_info = ''
        self.timezone = datetime.datetime.now().astimezone().tzinfo

        self.setWindowTitle("Unix时间戳转换")
        self.resize(500, 500)
        self.setup_ui()
        self.show()
        self.timer_1s = QTimer()
        self.timer_1s.timeout.connect(self.update_time_1s)
        self.timer_1s.start(1000)
        self.update_time_1s()
        self.timer_1ms = QTimer()
        self.timer_1ms.timeout.connect(self.update_time_1ms)
        self.timer_1ms.start(1)

    def update_time_1s(self):
        if self.mode != 'Live':
            return
        now_time = datetime.datetime.now()
        now_time = now_time.astimezone(zoneinfo.ZoneInfo(self.timezone))
        unix_timestamp = now_time.timestamp()
        time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
        self.unix_timestamp_edit.setText(str(unix_timestamp))
        self.time_str_edit.setText(time_str)


        self.utc_time_leabel.setText(now_time.strftime("%Y-%m-%dT%H:%M:%S %z"))
        self.day_leabel.setText(str(now_time.day))
        self.is_leap_leabel.setText("是" if now_time.isleap() else "否")

        self.week_leabel.setText(now_time.strftime("%A"))


    def update_time_1ms(self):
        if self.mode != 'Live':
            return
        now_time = datetime.datetime.now()
        millisecond = now_time.timestamp() * 1000
        self.millisecon_leabel.setText(str(millisecond))

    def eventFilter(self, obj, event):

        if obj in [self.unix_timestamp_edit, self.time_str_edit]:
            if event.type() == QEvent.Type.FocusIn:
                self.mode = 'Manual'

        return super().eventFilter(obj, event)

    def on_unix_edited(self):
        try:
            unix_timestamp = float(self.unix_timestamp_edit.text())
            dt = datetime.datetime.fromtimestamp(unix_timestamp)
            self.time_str_edit.setText(dt.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception:
            self.tbar_info = '输入的Unix时间戳格式错误'
            self.unix_timestamp_edit.setStyleSheet("border: 1px solid red;")

    def on_time_str_edited(self):
        try:
            dt = datetime.datetime.strptime(self.time_str_edit.text(), "%Y-%m-%d %H:%M:%S")
            self.unix_timestamp_edit.setText(str(dt.timestamp()))
        except Exception:
            self.tbar_info = '输入的日期时间格式错误'
            self.time_str_edit.setStyleSheet("border: 1px solid red;")

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        main_layout.addLayout(self.create_time_layout())
        main_layout.addLayout(self.create_func_layout())
        main_layout.addLayout(self.create_info_layout())
        main_layout.addLayout(self.create_tbar_layout())

    def create_time_layout(self):
        time_layout = QVBoxLayout()
        unix_layout = QHBoxLayout()

        unix_layout.addWidget(QLabel("Unix时间戳:"))
        self.unix_timestamp_edit = QLineEdit()
        self.unix_timestamp_edit.installEventFilter(self)
        self.unix_timestamp_edit.editingFinished.connect(self.on_unix_edited)
        unix_layout.addWidget(self.unix_timestamp_edit)
        unix_layout.addWidget(QPushButton("复制"))

        iso_layout = QHBoxLayout()
        iso_layout.addWidget(QLabel("日期时间:"))
        self.time_str_edit = QLineEdit()
        self.time_str_edit.installEventFilter(self)
        self.time_str_edit.editingFinished.connect(self.on_time_str_edited)
        iso_layout.addWidget(self.time_str_edit)
        iso_layout.addWidget(QPushButton("复制"))

        time_layout.addLayout(unix_layout)
        time_layout.addLayout(iso_layout)
        return time_layout

    def create_func_layout(self):
        func_layout = QVBoxLayout()
        func_layout_a = QHBoxLayout()
        func_layout_a.addWidget(QLabel("时区:"))
        combo = QComboBox()
        combo.addItems(["Local()", "Asia/Shanghai"])
        func_layout_a.addWidget(combo)

        func_layout_b = QHBoxLayout()
        func_layout_b.addWidget(QPushButton("🔄校准时间"))
        restore_button = QPushButton("⏰还原当前")
        restore_button.clicked.connect(self.restore)
        func_layout_b.addWidget(restore_button)
        func_layout_b.addWidget(QPushButton("⚙"))

        func_layout.addLayout(func_layout_a)
        func_layout.addLayout(func_layout_b)
        return func_layout

    def create_info_layout(self):
        info_layout = QVBoxLayout()
        info_layout.addWidget(QLabel("附加信息"))

        info_layout_1 = QHBoxLayout()
        info_layout_1.addWidget(QLabel("星期:"))
        self.week_leabel = QLabel("星期一")
        info_layout_1.addWidget(self.week_leabel)
        info_layout.addLayout(info_layout_1)

        info_layout_2 = QHBoxLayout()
        info_layout_2.addWidget(QLabel("年积日:"))
        self.day_leabel = QLabel("145")
        info_layout_2.addWidget(self.day_leabel)
        info_layout.addLayout(info_layout_2)
        info_layout_3 = QHBoxLayout()
        info_layout_3.addWidget(QLabel("闰年:"))
        self.is_leap_leabel = QLabel("否")
        info_layout_3.addWidget(self.is_leap_leabel)
        info_layout.addLayout(info_layout_3)
        info_layout_4 = QHBoxLayout()
        info_layout_4.addWidget(QLabel("UTC时间:"))
        self.utc_time_leabel = QLabel("2026‑05‑25T15:32:00+08:00")
        info_layout_4.addWidget(self.utc_time_leabel)
        info_layout.addLayout(info_layout_4)
        info_layout_5 = QHBoxLayout()
        info_layout_5.addWidget(QLabel("毫秒戳:"))
        self.millisecon_leabel = QLabel("1745251200000")
        info_layout_5.addWidget(self.millisecon_leabel)
        info_layout.addLayout(info_layout_5)
        return info_layout

    def create_tbar_layout(self):
        tbar_layout = QHBoxLayout()
        status_label = QLabel('正常')
        info_label = QLabel('附加信息')
        close_button = QPushButton('关闭')
        tbar_layout.addWidget(status_label)
        tbar_layout.addWidget(info_label)
        tbar_layout.addWidget(close_button)
        return tbar_layout

    def restore(self):
        self.mode = 'Live'
        self.update_time_1s()

# test code
if __name__ == "__main__":
    app = QApplication([])
    window = TimestampConverterMainWindow()
    app.exec()
    app.quit()


