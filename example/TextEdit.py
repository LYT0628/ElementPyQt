from PyQt6.QtWidgets import QApplication
from EPyQt.EWidgets import ETextEdit

if __name__ == "__main__":
    app = QApplication([])
    w = ETextEdit()
    w.setFixedSize(600, 400)
    w.show()
    app.exec()