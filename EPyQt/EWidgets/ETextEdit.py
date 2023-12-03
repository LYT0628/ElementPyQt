import logging

from PyQt6.QtCore import (
    Qt,
    QSize,
    QRect,
    pyqtSignal
)
from PyQt6.QtGui import (
    QPainter,
    QPaintEvent,
    QColor,
    QResizeEvent,
    QTextCursor,
    QTextCharFormat,
    QTextFormat
)
from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QApplication,
    QTextEdit,
)


class ETextEdit(QPlainTextEdit):
    resize_ = pyqtSignal(QRect)

    def __init__(self):
        super().__init__()

        self._lineNumberArea = LineNumberArea(self)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.highlightCurrentLine()

    # 计算行号(blockCount)的长度,
    # 这种数据得有唯一的可靠数据来源才行

    def resizeEvent(self, ev: QResizeEvent | None) -> None:
        super().resizeEvent(ev)
        self.resize_.emit(self.contentsRect())

    def highlightCurrentLine(self):
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(Qt.GlobalColor.yellow)
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)

        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()
        self.setExtraSelections([selection])

        # cursor = self.textCursor()
        # # selections = QPlainTextEdit.extraSelections()
        # # selection = QTextEdit.ExtraSelection()
        # cursor.movePosition(QTextCursor.MoveOperation.Down,
        #                     QTextCursor.MoveMode.MoveAnchor,
        #                     cursor.blockNumber())
        # cursor.movePosition(QTextCursor.MoveOperation.EndOfLine,
        #                     QTextCursor.MoveMode.KeepAnchor)
        # format = QTextCharFormat()
        # format.setBackground(Qt.GlobalColor.gray)
        # cursor.setCharFormat(format)


class LineNumberArea(QWidget):
    def __init__(self, editor: ETextEdit) -> None:
        super().__init__(editor)
        self._editor = editor
        self._editor.blockCountChanged.connect(self._updateArea)
        self._editor.updateRequest.connect(self._updateArea0)
        self._editor.resize_.connect(self._updateArea1)
        self._updateArea(0)
        self._updateArea0(dy=0)

    def sizeHint(self) -> QSize:
        return QSize(self._lineNumberAreaWidth(), 0)

    def paintEvent(self, ev: QPaintEvent | None) -> None:
        painter = QPainter(self)
        area = ev.rect()
        area.setWidth(self._lineNumberAreaWidth())
        painter.fillRect(area, Qt.GlobalColor.lightGray)
        block = self._editor.firstVisibleBlock()
        while block.isValid():
            block_number = block.blockNumber()
            block_top = self._editor.blockBoundingGeometry(block) \
                .translated(self._editor.contentOffset()).top()

            # Check if the position of the block is outside the visible area.
            if not block.isVisible() or block_top >= ev.rect().bottom():
                break

            # We want the line number for the selected line to be bold.
            if block_number == self._editor.textCursor().blockNumber():
                painter.setPen(QColor("#006000"))
            else:
                painter.setPen(QColor("#717171"))

            # Draw the line number right justified at the position of the line.
            paint_rect = QRect(0,
                               int(block_top),
                               self._lineNumberAreaWidth(),
                               self.fontMetrics().height())

            painter.drawText(paint_rect, Qt.AlignmentFlag.AlignCenter,
                             str(block_number + 1))

            block = block.next()

    def _lineNumberAreaWidth(self) -> int:
        digits: int = 1
        n: int = self._editor.blockCount() if self._editor.blockCount() > 1 else 1
        while n >= 10:
            n /= 10
            digits += 1
        space: int = 20 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    # update for number vary
    def _updateArea(self, blockCount: int = 0):
        # update editor
        margins = self._editor.viewportMargins()
        margins.setLeft(self._lineNumberAreaWidth())
        self._editor.setViewportMargins(margins)

    def _updateArea0(self, rect: QRect = None, dy: int = 0):
        if rect:
            self.update(0, rect.y(),
                        rect.width(), rect.height())
        else:
            self.scroll(0, dy)

        if rect and rect.contains(self._editor.viewport().rect()):
            self._updateArea()

    def _updateArea1(self, cr: QRect):
        rect = QRect(cr.left(), cr.top(), self._lineNumberAreaWidth(), cr.height())
        self.setGeometry(rect)


