from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from EPyQt.EWidgets import EShell, ETextEdit, EDefaultWindow

if __name__ == "__main__":
    app = QApplication([])
    w = EDefaultWindow()
    wg = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(ETextEdit())
    layout.addWidget(EShell())
    wg.setLayout(layout)
    w.setWidget(wg)
    w.setFixedSize(600, 500)
    w.show()
    app.exec()
