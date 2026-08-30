from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPlainTextEdit, QPushButton, QLabel, QFileDialog)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from .logic import generate_qr_png


class QRGeneratorMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("二维码生成器")
        self.resize(500, 600)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(8)

        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("在此输入文本或网址")
        main.addWidget(QLabel("输入"))
        main.addWidget(self.input)

        btn_row = QHBoxLayout()
        gen = QPushButton("生成")
        gen.clicked.connect(self.generate)
        btn_row.addWidget(gen)
        btn_row.addStretch(1)
        main.addLayout(btn_row)

        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setMinimumHeight(200)
        main.addWidget(self.preview, 1)

        save_row = QHBoxLayout()
        save = QPushButton("保存为 PNG")
        save.clicked.connect(self.save)
        save_row.addWidget(save)
        save_row.addStretch(1)
        main.addLayout(save_row)

        self.status = QLabel("")
        main.addWidget(self.status)
        self._img = None

    def generate(self):
        text = self.input.toPlainText().strip()
        if not text:
            self.status.setText("请输入内容")
            return
        try:
            png_data, img = generate_qr_png(text)
            pix = QPixmap()
            pix.loadFromData(png_data)
            self.preview.setPixmap(pix.scaled(
                300, 300,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation))
            self._img = img
            self.status.setText("生成完成")
        except Exception as e:
            self.status.setText(f"错误: {e}")

    def save(self):
        if not self._img:
            self.status.setText("请先生成二维码")
            return
        path, _ = QFileDialog.getSaveFileName(self, "保存二维码", "qrcode.png", "PNG 图片 (*.png)")
        if path:
            self._img.save(path)
            self.status.setText(f"已保存: {path}")
