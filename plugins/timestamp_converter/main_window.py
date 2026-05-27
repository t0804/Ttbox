import datetime
import calendar
import time
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QApplication, QComboBox, QFrame)
from PySide6.QtCore import Qt, QTimer, QEvent
import requests


WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
UTC_OFFSET_LIST = [
    "UTC-12:00", "UTC-11:00", "UTC-10:00", "UTC-09:30", "UTC-09:00",
    "UTC-08:00", "UTC-07:00", "UTC-06:00", "UTC-05:00", "UTC-04:00",
    "UTC-03:30", "UTC-03:00", "UTC-02:00", "UTC-01:00", "UTC±00:00",
    "UTC+01:00", "UTC+02:00", "UTC+03:00", "UTC+03:30", "UTC+04:00",
    "UTC+04:30", "UTC+05:00", "UTC+05:30", "UTC+05:45", "UTC+06:00",
    "UTC+06:30", "UTC+07:00", "UTC+08:00", "UTC+08:45", "UTC+09:00",
    "UTC+09:30", "UTC+10:00", "UTC+11:00", "UTC+12:00", "UTC+12:45",
    "UTC+13:00", "UTC+13:45", "UTC+14:00"
]
NTP_SERVERS = [
    "timeapi.org"
]


class TimestampConverterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mode = 'Live'  # 状态机模式 Live or Manual
        self.tbar_info = ''
        self._now_time = datetime.datetime.now().astimezone()
        self._current_timezone = datetime.datetime.now().astimezone().tzinfo

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
        self._now_time = datetime.datetime.now().astimezone(self._current_timezone)
        self.refresh_display()

    def refresh_display(self):
        now_time = self._now_time
        now_time = now_time.astimezone(self._current_timezone)
        unix_timestamp = now_time.timestamp()
        time_str = now_time.strftime("%Y-%m-%d %H:%M:%S")
        self.unix_timestamp_edit.setText(str(unix_timestamp))
        self.time_str_edit.setText(time_str)
        time_str = now_time.strftime("%Y-%m-%dT%H:%M:%S%z")
        time_str = time_str[:-2] + ':' + time_str[-2:]
        self.utc_time_leabel.setText(time_str)
        self.day_leabel.setText(str(now_time.timetuple().tm_yday))
        self.is_leap_leabel.setText("是" if calendar.isleap(now_time.year) else "否")
        self.week_leabel.setText(WEEKDAYS[now_time.weekday()]+f"({now_time.strftime('%A')})")
        self.millisecon_leabel.setText(str(now_time.timestamp() * 1000))

    def update_time_1ms(self):
        if self.mode != 'Live':
            return
        self.millisecon_leabel.setText(str(time.time()))

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
            self._now_time = dt
            self.refresh_display()
        except Exception:
            self.tbar_info = '输入的Unix时间戳格式错误'
            self.unix_timestamp_edit.setStyleSheet("border: 1px solid red;")

    def on_time_str_edited(self):
        try:
            dt = datetime.datetime.strptime(self.time_str_edit.text(), "%Y-%m-%d %H:%M:%S")
            self._now_time = dt
            self.refresh_display()
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
        main_layout.addWidget(self.create_tbar_layout())

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

        current_timezone = self._now_time.tzinfo
        utc_offset_list = [f"Local({current_timezone})"] + UTC_OFFSET_LIST
        combo.addItems(utc_offset_list)
        combo.currentIndexChanged.connect(self.on_combo_changed)
        func_layout_a.addWidget(combo)

        func_layout_b = QHBoxLayout()
        calibration_time =QPushButton("🔄校准时间")
        calibration_time.clicked.connect(self.ntp_calibration)
        func_layout_b.addWidget(calibration_time)
        restore_button = QPushButton("⏰还原当前")
        restore_button.clicked.connect(self.restore)
        func_layout_b.addWidget(restore_button)
        setting_button = QPushButton("⚙")
        setting_button.clicked.connect(self.show_setting_frame)
        func_layout_b.addWidget(setting_button)

        func_layout.addLayout(func_layout_a)
        func_layout.addLayout(func_layout_b)
        self.ntp_frame = self.create_ntp_frame()
        self.ntp_frame.setVisible(False)
        func_layout.addWidget(self.ntp_frame)
        return func_layout

    def create_ntp_frame(self):
        frame = QFrame()
        # frame.setStyleSheet("border: 1px solid #000; padding: 10px;")
        frame_layout = QVBoxLayout(frame)
        layout_1 = QHBoxLayout()
        layout_1.addWidget(QLabel("NTP服务器:"))
        combo = QComboBox()
        combo.addItems(NTP_SERVERS)
        layout_1.addWidget(combo)
        layout_2 = QHBoxLayout()
        layout_2.addWidget(QLabel('超时:'))
        layout_2.addWidget(QLineEdit('10'))
        layout_2.addWidget(QLabel('秒'))
        frame_layout.addLayout(layout_1)
        frame_layout.addLayout(layout_2)
        return frame

    def show_setting_frame(self):
        self.ntp_frame.setVisible(not self.ntp_frame.isVisible())

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
        self.tbar_frame = QFrame()
        self.tbar_frame.setVisible(False)
        tbar_layout = QHBoxLayout(self.tbar_frame)
        status_label = QLabel('正常')
        info_label = QLabel('附加信息')
        close_button = QPushButton('关闭')
        close_button.clicked.connect(self.close_tbar)
        tbar_layout.addWidget(status_label)
        tbar_layout.addWidget(info_label)
        tbar_layout.addWidget(close_button)
        return self.tbar_frame

    def close_tbar(self):
        self.tbar_frame.setVisible(False)
    def restore(self):
        self.mode = 'Live'
        self.update_time_1s()

    def on_combo_changed(self, index):
        if index == 0:
            self._now_time = datetime.datetime.now().astimezone()
            self._current_timezone = self._now_time.tzinfo
            self.refresh_display()
        else:
            # 根据索引获取时区偏移，生成时区对象
            offset_str = UTC_OFFSET_LIST[index - 1]
            current_timezone = self.utc_str_to_timezone(offset_str)
            self._now_time = datetime.datetime.now().astimezone(current_timezone)
            self._current_timezone = self._now_time.tzinfo
            self.refresh_display()

    def offset_to_utc_str(self, offset) -> str:
        """
        将 timedelta 类型的时区偏移 转为 UTC±HH:MM 格式字符串
        """
        total_seconds = offset.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int(abs(total_seconds) % 3600 // 60)
        if hours > 0:
            sign = "+"
        elif hours < 0:
            sign = "-"
            hours = abs(hours)
        else:
            sign = "±"
        return f"UTC{sign}{hours:02d}:{minutes:02d}"

    def utc_str_to_timezone(self, utc_str):
        """
        将 UTC 偏移字符串 转为 Python timezone 对象
        支持：UTC-12:00, UTC-03:30, UTC+09:00, UTC±00:00 等格式
        """
        # 清理字符串，只保留符号、小时、分钟
        s = utc_str.replace("UTC", "").replace("±", "+")
        if s.startswith("-"):
            sign = -1
        else:
            sign = 1
        s = s[1:]
        # 拆分小时、分钟
        hh, mm = s.split(":")
        hours = int(hh)
        minutes = int(mm)
        # 计算偏移
        delta = datetime.timedelta(hours=sign * hours, minutes=sign * minutes)
        return datetime.timezone(delta)

    def ntp_calibration(self):
        # 校准时间
        self.tbar_frame.setVisible(True)
        pass
# test code
if __name__ == "__main__":
    app = QApplication([])
    window = TimestampConverterMainWindow()
    app.exec()
    app.quit()


