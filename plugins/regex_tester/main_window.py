from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QTextEdit)
from PySide6.QtGui import QTextCursor, QTextCharFormat, QColor
from .logic import find_matches, compile_pattern


class RegexTesterMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("正则测试器")
        self.resize(800, 600)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(8)

        self.pattern = QLineEdit()
        self.pattern.setPlaceholderText("正则表达式，例如 (\\d+)")
        main.addWidget(QLabel("正则表达式"))
        main.addWidget(self.pattern)

        self.text = QTextEdit()
        self.text.setPlaceholderText("测试文本")
        main.addWidget(QLabel("测试文本"))
        main.addWidget(self.text, 1)

        row = QHBoxLayout()
        test = QPushButton("测试")
        test.clicked.connect(self.run)
        row.addWidget(test)
        row.addStretch(1)
        main.addLayout(row)
        self.status = QLabel("")
        main.addWidget(self.status)

    def run(self):
        pat = self.pattern.text()
        src = self.text.toPlainText()
        self.text.setExtraSelections([])
        if not pat:
            self.status.setText("请输入正则表达式")
            return
        rx, err = compile_pattern(pat)
        if err:
            self.status.setText(f"正则错误: {err}")
            return
        matches = find_matches(pat, src)
        sels = []
        for start, end, _ in matches:
            c = QTextCursor(self.text.document())
            c.setPosition(start)
            c.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
            f = QTextCharFormat()
            f.setBackground(QColor("#1a7f3720"))
            f.setForeground(QColor("#1a7f37"))
            s = QTextEdit.ExtraSelection()
            s.cursor = c
            s.format = f
            sels.append(s)
        self.text.setExtraSelections(sels)
        self.status.setText(f"匹配 {len(matches)} 处")
