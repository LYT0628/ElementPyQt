from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class EWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)


if __name__ == "__main__":
    app = QApplication([])
    w = EWindow()
    w.setFixedSize(600, 400)
    w.show()
    app.exec()
