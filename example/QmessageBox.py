from PyQt6.QtWidgets import QApplication, QMessageBox, QWidget
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from EPyQt.EWidgets._rc import res_rc
if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.setFixedSize(200, 200)
    w.show()
    # btn = QMessageBox.question(w, "title", "message",
    #                            buttons=QMessageBox.StandardButton.Discard
    #                                    | QMessageBox.StandardButton.NoToAll
    #                                    | QMessageBox.StandardButton.Ignore, )
    dlg = QMessageBox(w)
    dlg.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
    """)
    # dlg.setWindowOpacity(0.6)
    dlg.set
    dlg.setWindowFlags(Qt.WindowType.WindowType_Mask)
    # dlg.setWindowFlags(Qt.WindowType.SubWindow)
    # dlg.setWindowFlags(Qt.WindowType.Sheet)
    dlg.setWindowTitle("question")
    dlg.setText("Button order is platform-dependent.")
    dlg.setStandardButtons(
        QMessageBox.StandardButton.Help |
        QMessageBox.StandardButton.Escape
    )

    dlg.setModal(False)

    # dlg.setIcon(QMessageBox.Icon.Information)
    # dlg.setIcon(QMessageBox.Icon.Critical)
    icon = QPixmap(":/epyqt/icon/question.svg")
    icon = icon.scaled(60, 60)
    dlg.setIconPixmap(icon)
    button = dlg.exec()

    app.exec()
