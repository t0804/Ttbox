from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel,
                               QTextEdit)
from PySide6.QtGui import QTextCharFormat, QTextCursor, QColor
from PySide6.QtCore import Qt


def _lcs_opcodes(a, b):
    # ponytail: true LCS (not Ratcliff-Obershelp) so diffs localize to the real change.
    # O(n*m) time/memory; fine for toolbox-sized text.
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        ai = a[i]
        row, nxt = dp[i], dp[i + 1]
        for j in range(m - 1, -1, -1):
            row[j] = nxt[j + 1] + 1 if ai == b[j] else max(nxt[j], row[j + 1])
    raw = []
    i = j = 0
    while i < n and j < m:
        if a[i] == b[j]:
            raw.append(("equal", i, i + 1, j, j + 1)); i += 1; j += 1
        elif dp[i + 1][j] >= dp[i][j + 1]:
            raw.append(("delete", i, i + 1, j, j)); i += 1
        else:
            raw.append(("insert", i, i, j, j + 1)); j += 1
    while i < n:
        raw.append(("delete", i, i + 1, j, j)); i += 1
    while j < m:
        raw.append(("insert", i, i, j, j + 1)); j += 1
    out = []
    for tag, i1, i2, j1, j2 in raw:
        if out and out[-1][0] == tag:
            p = out[-1]
            out[-1] = (tag, p[1], i2, p[3], j2)
        else:
            out.append((tag, i1, i2, j1, j2))
    return out


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
        for tag, i1, i2, j1, j2 in _lcs_opcodes(a, b):
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
