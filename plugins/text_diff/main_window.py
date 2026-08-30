from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                               QTextEdit)
from PySide6.QtCore import Qt
from .logic import lcs_opcodes


class TextDiffMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文本对比")
        self.resize(800, 600)
        self._suppress = False
        self.setup_ui()
        self._refresh()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main = QVBoxLayout(central)
        main.setContentsMargins(10, 10, 10, 10)
        main.setSpacing(8)

        self.top = QTextEdit()
        self.top.setPlaceholderText("参考文本（以上面的为准）")
        self.top.textChanged.connect(self._refresh)
        main.addWidget(QLabel("原文本"))
        main.addWidget(self.top)

        self.bottom = QTextEdit()
        self.bottom.setPlaceholderText("对比文本，输入即实时对比")
        self.bottom.textChanged.connect(self._refresh)
        main.addWidget(QLabel("对比文本"))
        main.addWidget(self.bottom, 1)

    def _highlight(self, edit, ranges, fmt):
        sels = []
        for s, e in ranges:
            c = QTextCursor(edit.document())
            c.setPosition(s)
            c.setPosition(e, QTextCursor.MoveMode.KeepAnchor)
            sel = QTextEdit.ExtraSelection()
            sel.cursor = c
            sel.format = fmt()
            sels.append(sel)
        edit.setExtraSelections(sels)

    def _refresh(self):
        if self._suppress:
            return
        self._suppress = True
        a = self.top.toPlainText()
        b = self.bottom.toPlainText()
        top_red, bot_green = [], []
        for tag, i1, i2, j1, j2 in lcs_opcodes(a, b):
            if tag == "delete":
                top_red.append((i1, i2))
            elif tag in ("insert", "replace"):
                bot_green.append((j1, j2))

        def red():
            f = QTextCharFormat()
            f.setForeground(QColor("#cf222e"))
            f.setFontStrikeOut(True)
            return f

        def green():
            f = QTextCharFormat()
            f.setForeground(QColor("#1a7f37"))
            f.setBackground(QColor("#1a7f3720"))
            return f

        self._highlight(self.top, top_red, red)
        self._highlight(self.bottom, bot_green, green)
        self._suppress = False
