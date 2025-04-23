from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class Main_window(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowType.Window)
        label1 = QLabel('Test')
        btn1 = QPushButton('Test')
        layout = QVBoxLayout()
        layout.addWidget(label1, btn1)
        self.setLayout(layout)
