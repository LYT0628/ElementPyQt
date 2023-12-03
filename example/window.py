from PyQt6.QtWidgets import QApplication
from EPyQt.EWidgets import ETextEdit
from  EPyQt.EWidgets import EDefaultWindow


if __name__ == "__main__":
    app = QApplication([])
    w = EDefaultWindow()
    w.setWidget(ETextEdit())
    w.show()
    app.exec()