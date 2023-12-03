from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class EShell(QTextEdit):
    def __init__(self):
        super().__init__()
        self._font = QFont()
        self._proc = QProcess()
        self._pos = 0
        self._lastInput = QByteArray()

        self.setStyleSheet("""
            background-color: rgb(0,0,0);
            color: rgb(255,255,255);
            border: 0px;
        """)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.resize(1000, 700)
        self.setWindowTitle("bash")
        self._font.setFamily("Times New Roman")
        self._font.setPixelSize(14)
        self.setFont(self._font)

        self._proc.readyReadStandardOutput.connect(self._readyReadStrandOutput)
        self._proc.readyReadStandardError.connect(self._readyReadStrandError)
        self._proc.start("cmd")
        if QSysInfo.productType() == "windows":
            print("win")
            self._proc.start("cmd")
        elif QSysInfo.productType() == "Linux":
            self._proc.start("bash")

        cursor = self.textCursor()
        block_format = QTextBlockFormat()

        cursor.setBlockFormat(block_format)
        self.setTextCursor(cursor)

    def keyPressEvent(self, e):
        cursor = self.textCursor()
        if e.key() == Qt.Key.Key_Return or e.key() == Qt.Key.Key_Enter:
            e.ignore()
            cursor.setPosition(self._pos, QTextCursor.MoveMode.MoveAnchor)
            cursor.movePosition(QTextCursor.MoveOperation.End, QTextCursor.MoveMode.KeepAnchor)
            str = cursor.selectedText() + "\r\n"

            self._proc.write(str.encode("utf-8"))

        elif e.key() == Qt.Key.Key_Backspace and cursor.position() <= self._pos:
            return
        elif e.key() == Qt.Key.Key_Delete and cursor.position() <= self._pos:
            return
        else:
            return super().keyPressEvent(e)

    def _readyReadStrandOutput(self):

        bs = self._proc.readAllStandardOutput()
        string = bs.data().decode("gbk")
        print(string)
        if len(string) > 0:
            self.setTextColor(Qt.GlobalColor.white)
            self.append(string)

            self.moveCursor(QTextCursor.MoveOperation.End)
            self._pos = self.textCursor().position()

    def _readyReadStrandError(self, ):

        bs = self._proc.readAllStandardError()
        string = bs.data().decode("gbk")
        print(string)
        if len(string) > 0:
            self.setTextColor(Qt.GlobalColor.red)
            self.append(string)

            self.moveCursor(QTextCursor.MoveOperation.End)
            self._pos = self.textCursor().position()
