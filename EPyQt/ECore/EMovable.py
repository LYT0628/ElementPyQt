from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPoint, Qt


# 可被鼠标移动的，可以接受鼠标信号而产生移动的
class EMovable(QWidget):
    def move(self, pos: QPoint):
        super().move(pos)


class EWindowMovable(EMovable):
    def move(self, pos: QPoint):
        if self.windowState() == Qt.WindowState.WindowMaximized or self.windowState() == Qt.WindowState.WindowFullScreen:
            return
        super().move(pos)