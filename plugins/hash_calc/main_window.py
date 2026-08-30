from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPlainTextEdit, QPushButton, QLabel, QComboBox,
                               QFileDialog)
from .logic import calc_hash


class HashCalcMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("哈希计算")
        self.resize(800, 500)
        self._file = None
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(8)

        self.input = QPlainTextEdit()
        self.input.setPlaceholderText("在此输入文本，或点击下方选择文件")
        main.addWidget(QLabel("输入"))
        main.addWidget(self.input)

        row = QHBoxLayout()
        row.addWidget(QLabel("算法:"))
        self.algo = QComboBox()
        self.algo.addItems(["md5", "sha1", "sha256", "sha512"])
        row.addWidget(self.algo)
        file_btn = QPushButton("选择文件")
        file_btn.clicked.connect(self.pick_file)
        row.addWidget(file_btn)
        calc = QPushButton("计算")
        calc.clicked.connect(self.calc)
        row.addWidget(calc)
        row.addStretch(1)
        main.addLayout(row)

        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        main.addWidget(QLabel("结果"))
        main.addWidget(self.output, 1)
        self.status = QLabel("")
        main.addWidget(self.status)

    def pick_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if path:
            self._file = path
            self.input.clear()
            self.status.setText(f"已选择文件: {path}")

    def calc(self):
        try:
            result = calc_hash(
                text=self.input.toPlainText() if not self._file else None,
                file_path=self._file,
                algorithm=self.algo.currentText(),
            )
            self.output.setPlainText(result)
            self.status.setText("计算完成")
        except Exception as e:
            self.status.setText(f"错误: {e}")
