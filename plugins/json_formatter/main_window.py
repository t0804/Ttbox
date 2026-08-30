from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPlainTextEdit, QPushButton, QLabel)
from PySide6.QtCore import Qt
from .logic import format_json, compact_json, verify_json


class JsonFormatterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JSON 格式化")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(8)

        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("在此粘贴 JSON")
        main.addWidget(QLabel("输入"))
        main.addWidget(self.input)

        btn_row = QHBoxLayout()
        fmt = QPushButton("格式化")
        fmt.clicked.connect(self.do_format)
        comp = QPushButton("压缩")
        comp.clicked.connect(self.do_compact)
        verify = QPushButton("校验")
        verify.clicked.connect(self.do_verify)
        btn_row.addWidget(fmt)
        btn_row.addWidget(comp)
        btn_row.addWidget(verify)
        btn_row.addStretch(1)
        main.addLayout(btn_row)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        main.addWidget(QLabel("输出"))
        main.addWidget(self.output, 1)

        self.status = QLabel("")
        main.addWidget(self.status)

    def do_format(self):
        result, err = format_json(self.input.toPlainText())
        if err:
            self.status.setText(f"错误: 第 {err.lineno} 行第 {err.colno} 列: {err.msg}")
            return
        self.output.setPlainText(result)
        self.status.setText("格式化完成")

    def do_compact(self):
        result, err = compact_json(self.input.toPlainText())
        if err:
            self.status.setText(f"错误: 第 {err.lineno} 行第 {err.colno} 列: {err.msg}")
            return
        self.output.setPlainText(result)
        self.status.setText("压缩完成")

    def do_verify(self):
        ok, err = verify_json(self.input.toPlainText())
        if err:
            self.status.setText(f"不合法: 第 {err.lineno} 行第 {err.colno} 列: {err.msg}")
        else:
            self.status.setText("合法 JSON")
