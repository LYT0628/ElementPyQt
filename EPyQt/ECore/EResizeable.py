from abc import abstractmethod

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPoint, Qt, QMargins, QRect

from EPyQt.ECore.EQt import Edge


class EResizable(QWidget):
    def __init__(self):
        super().__init__()
        self._pos: QPoint | None = None
        self._pressed: bool = False
        self._direction = None
        # 移动策略列表， 作为观察者， able为策略提供必要的信息
        self._moveObserver = []

    @abstractmethod
    def resize_(self, pos: QPoint):
        pass

    def mousePressEvent(self, ev, mouseEv=None):
        if ev.button() == Qt.MouseButton.LeftButton:
            self._pos = ev.pos()
            self._pressed = True
        super().mousePressEvent(ev)

    def addMoveObserver(self, a0):
        self._moveObserver.append(a0)

    def mouseReleaseEvent(self, ev, mouseEv=None):
        self._pos = None
        self._pressed = False
        super().mouseReleaseEvent(ev)


class EWindowResizable(EResizable):

    def resize_(self, pos: QPoint):
        # 计算差值
        pos = pos - self._pos

        x_pos, y_pos = pos.x(), pos.y()
        # 获得原本的大小
        geometry = self.geometry()
        x, y, w, h = geometry.x(), geometry.y(), geometry.width(), geometry.height()

        for strategy in self._moveObserver:
            if not strategy.isNeed(self._direction):
                continue
            dx, dy, dw, dh = strategy.vary()
            x += x_pos * dx
            y += y_pos * dy
            w += x_pos * dw
            h += y_pos * dh
            self.setGeometry(QRect(x, y, w, h))

    def __init__(self):
        super().__init__()
        self._margins = 5
        self._direction = None
        self._varX: int = 0
        self._varY: int = 0
        self.varW: int = 0
        self.varH: int = 0

        self.setContentsMargins(QMargins(self._margins, self._margins, self._margins, self._margins))
        self.addMoveObserver(LeftTopResizeStrategy())
        self.addMoveObserver(RightTopResizeStrategy())
        self.addMoveObserver(RightBottomResizeStrategy())
        self.addMoveObserver(LeftBottomResizeStrategy())

        self.addMoveObserver(LeftResizeStrategy())
        self.addMoveObserver(TopResizeStrategy())
        self.addMoveObserver(RightResizeStrategy())
        self.addMoveObserver(BottomResizeStrategy())

    def mouseMoveEvent(self, ev, mouseEv=None):
        super().mouseMoveEvent(ev)

        if self.isMaximized() or self.isFullScreen():
            self._direction = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            return

        if ev.buttons() == Qt.MouseButton.LeftButton and self._pressed:
            self.resize_(ev.pos())
            # 及时更新数据
            self._pos = ev.pos()
            return

        for strategy in self._moveObserver:
            strategy.markPosition(ev.pos(), self)


class ResizeStrategy:

    @abstractmethod
    def vary(self) -> (int, int, int, int):
        pass

    @abstractmethod
    def cursor(self) -> Qt.CursorShape:
        pass

    @abstractmethod
    def isNeed(self, a0) -> bool:
        pass

    @abstractmethod
    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        pass


class LeftTopResizeStrategy(ResizeStrategy):

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if x_pos <= margins and y_pos <= margins:
            # 左上角
            widget._direction = Edge.LEFT_TOP
            widget.setCursor(Qt.CursorShape.SizeFDiagCursor)

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.LEFT_TOP

    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 1, 1, -1, -1


class RightTopResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 0, 1, 1, -1

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.RIGHT_TOP

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if wm <= x_pos and y_pos <= margins:
            widget._direction = Edge.RIGHT_TOP
            widget.setCursor(Qt.CursorShape.SizeBDiagCursor)


class LeftBottomResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 1, 0, -1, 1

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.LEFT_BOTTOM

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if x_pos <= margins and hm <= y_pos:
            # 左下角
            widget._direction = Edge.LEFT_BOTTOM
            widget.setCursor(Qt.CursorShape.SizeBDiagCursor)


class RightBottomResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 0, 0, 1, 1

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.RIGHT_BOTTOM

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if wm <= x_pos <= widget.width() and hm <= y_pos <= widget.height():
            # 右下角
            widget._direction = Edge.RIGHT_BOTTOM
            widget.setCursor(Qt.CursorShape.SizeFDiagCursor)


class LeftResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 1, 0, -1, 0

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.LEFT

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if 0 <= x_pos <= margins and margins <= y_pos <= hm:
            # 左边
            widget._direction = Edge.LEFT
            widget.setCursor(Qt.CursorShape.SizeHorCursor)


class RightResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 0, 0, 1, 0

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.RIGHT

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if wm <= x_pos <= widget.width() and margins <= y_pos <= hm:
            # 右边
            widget._direction = Edge.RIGHT
            widget.setCursor(Qt.CursorShape.SizeHorCursor)


class TopResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 0, 1, 0, -1

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.TOP

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if margins <= x_pos <= wm  and 0 <= y_pos <= margins:
            # 上面
            widget._direction = Edge.TOP
            widget.setCursor(Qt.CursorShape.SizeVerCursor)


class BottomResizeStrategy(ResizeStrategy):
    def cursor(self) -> Qt.CursorShape:
        return Qt.CursorShape.SizeFDiagCursor

    def vary(self) -> (int, int, int, int):
        return 0, 0, 0, 1

    def isNeed(self, a0: Edge) -> bool:
        return a0 == Edge.BOTTOM

    def markPosition(self, pos: QPoint, widget: QWidget) -> None:
        if not hasattr(widget, "_direction"):
            widget._direction = None
        margins = 5  # 为光标留出合适的区域
        # 窗口左上角
        x_pos, y_pos = pos.x(), pos.y()
        # 窗口右下角
        wm, hm = widget.width() - margins, widget.height() - margins
        if (margins <= x_pos <= wm
                and hm <= y_pos <= widget.height()):
            # 下面
            widget._direction = Edge.BOTTOM
            widget.setCursor(Qt.CursorShape.SizeVerCursor)
