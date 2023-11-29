import os

from PyQt6.QtWidgets import QPushButton, QWidget, QHBoxLayout,QTextEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QFile

from EPyQt import  EUtils
from EPyQt.EBootStrap._load import load



class PrimaryButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        # self.setObjectName('primary')
        self.setProperty('color', 'primary')


class SecondButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        # self.setObjectName('second')
        self.setProperty('color', 'secondary')


class InfoButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setProperty('color', 'info')


class SuccessButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setProperty('color', 'success')


class WarningButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setProperty('color', 'warning')


class DangerButton(QPushButton):
    def __init__(self, text: str):
        super().__init__(text)
        self.setProperty('color', 'danger')


from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':

    app = QApplication([])
    w = QWidget()
    h_box = QHBoxLayout()
    default_btn = QPushButton('default')
    # primary_btn = PrimaryButton("Primary")
    second_btn = SecondButton("Second")
    info_btn = InfoButton("Info")
    success_btn = SuccessButton("Success")
    warning_btn = WarningButton("warning")
    danger_btn = DangerButton("danger")
    primary_btn = PrimaryButton("Primary")
    h_box.addWidget(default_btn)

    h_box.addWidget(second_btn)
    h_box.addWidget(success_btn)
    h_box.addWidget(info_btn)
    h_box.addWidget(warning_btn)
    h_box.addWidget(danger_btn)
    h_box.addWidget(primary_btn)
    te = QTextEdit()
    h_box.addWidget(te)
    w.setLayout(h_box)

    app.setStyleSheet(load())
    w.show()
    app.exec()
