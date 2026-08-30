from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPlainTextEdit, QPushButton, QLabel)
from .logic import b64_encode, b64_decode, url_encode, url_decode


class Base64UrlMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base64 / URL 编解码")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(8)

        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("在此输入文本")
        main.addWidget(QLabel("输入"))
        main.addWidget(self.input)

        btn = QHBoxLayout()
        for text, slot in (("Base64编码", self._b64_enc), ("Base64解码", self._b64_dec),
                           ("URL编码", self._url_enc), ("URL解码", self._url_dec)):
            b = QPushButton(text)
            b.clicked.connect(slot)
            btn.addWidget(b)
        btn.addStretch(1)
        main.addLayout(btn)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        main.addWidget(QLabel("输出"))
        main.addWidget(self.output, 1)
        self.status = QLabel("")
        main.addWidget(self.status)

    def _b64_enc(self):
        self.output.setPlainText(b64_encode(self.input.toPlainText()))
        self.status.setText("Base64 编码完成")

    def _b64_dec(self):
        try:
            self.output.setPlainText(b64_decode(self.input.toPlainText()))
            self.status.setText("Base64 解码完成")
        except Exception as e:
            self.status.setText(f"解码失败（不是合法 Base64）: {e}")

    def _url_enc(self):
        self.output.setPlainText(url_encode(self.input.toPlainText()))
        self.status.setText("URL 编码完成")

    def _url_dec(self):
        self.output.setPlainText(url_decode(self.input.toPlainText()))
        self.status.setText("URL 解码完成")
