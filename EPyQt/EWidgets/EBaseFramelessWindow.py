from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

from EPyQt.ECore import EQt
# from EPyQt.EWidgets._rc import res_rc
from EPyQt.EWidgets._rc import res_rc
from EPyQt.ECore.EMovable import EWindowMovable
from EPyQt.ECore.EResizeable import EWindowResizable


#
# class EAbstractTitleBar(QWidget, EMovable):
#     # 通知窗口最小化
#     WindowMinimized = pyqtSignal()
#     # 通知窗口最大化
#     windowMaximized = pyqtSignal()
#     # 通知窗口回复正常
#     windowNormalized = pyqtSignal()
#     # 通知窗口关闭
#     windowClosed = pyqtSignal()
#     # 通知窗口移动， 提交提供的坐标差(新-旧)
#     windowMoved = pyqtSignal(QPoint)
#
#
# class EAbstractFramelessWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         # 标题栏
#         self._titleBar = ETitleBar()
#         # 主要组件， 和标题栏一起组成FramelessWindow
#         self._widget = None
#         # 移动策略。 控制窗口的移动
#         self._moveStrategy = None
#         # 大小改变策略， 控制狂口大小改变
#         self._resizeStrategy = None
#
#     @abstractmethod
#     def setWidget(self, widget: QWidget):
#         # 设置组件
#         pass
#
#     @abstractmethod
#     def setTitleBar(self, titleBar: EAbstractTitleBar):
#         # 设置标题栏
#         pass


class ETitleBar(QWidget):
    # 通知窗口最小化
    WindowMinimized = pyqtSignal()
    # 通知窗口最大化
    windowMaximized = pyqtSignal()
    # 通知窗口回复正常
    windowNormalized = pyqtSignal()
    # 通知窗口关闭
    windowClosed = pyqtSignal()
    # 通知窗口移动， 提交提供的坐标差(新-旧)
    windowMoved = pyqtSignal(QPoint)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._iconMargins = None
        self._closeButton = None
        self._maximumButton = None
        self._minimumButton = None
        self._iconLabel = None
        self._pos = None
        self._iconSize = 20
        self._status = EQt.WindowState.Normal

        self._initialUi()
        self._setupSignal()
        self._setupUi()

    def _setupUi(self):

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._iconLabel)
        layout.addWidget(self.titleLabel)

        # 中间伸缩条
        layout.addSpacerItem(QSpacerItem(
            40, 20,
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum))

        layout.addWidget(self._minimumButton)
        layout.addWidget(self._maximumButton)
        layout.addWidget(self._closeButton)

        self.setHeight()

    def _setupSignal(self):
        self._minimumButton.clicked.connect(lambda: self.WindowMinimized.emit())
        self._maximumButton.clicked.connect(self.maximized)
        self._closeButton.clicked.connect(lambda: self.windowClosed.emit())

    def _initialButtons(self):
        self._minimumButton = QPushButton(self)
        self._minimumButton.setIcon(QIcon(":/epyqt/icon/minimize.svg"))
        self._maximumButton = QPushButton(self)
        self._maximumButton.setIcon(QIcon(":/epyqt/icon/maximize-1.svg"))
        self._closeButton = QPushButton(self)
        self._closeButton.setIcon(QIcon(":/epyqt/icon/close.svg"))

    def _initialTitle(self):
        # 窗口标题
        self.titleLabel = QLabel(self)
        self.titleLabel.setMargin(2)

    def _initialIcon(self):
        # 窗口图标
        self._iconLabel = QLabel("xxx")
        icon = QPixmap(":/epyqt/icon/logo.svg")
        icon = icon.scaled(self._iconSize, self._iconSize)
        self._iconLabel.setPixmap(icon)
        self._iconLabel.setContentsMargins(20, 0, 0, 0)

    def _initialUi(self):
        # 设置默认背景颜色,否则由于受到父窗口的影响导致透明
        self.setAutoFillBackground(True)

        self._initialButtons()
        self._initialIcon()
        self._initialTitle()
        size_policy = self.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Fixed)
        self.setSizePolicy(size_policy)

    def maximized(self):
        # 最大化
        if self._status == EQt.WindowState.Normal:
            self._status = EQt.WindowState.Maximum
            self.windowMaximized.emit()
        else:  # 还原
            self.windowNormalized.emit()
            self._status = EQt.WindowState.Normal

    def setHeight(self, height=38):
        """设置标题栏高度"""
        self.setMinimumHeight(height)
        self.setMaximumHeight(height)
        # 设置右边按钮的大小
        self._minimumButton.setMinimumSize(height, height)
        self._minimumButton.setMaximumSize(height, height)
        self._maximumButton.setMinimumSize(height, height)
        self._maximumButton.setMaximumSize(height, height)
        self._closeButton.setMinimumSize(height, height)
        self._closeButton.setMaximumSize(height, height)

    def setTitle(self, title):
        """设置标题"""
        self.titleLabel.setText(title)

    def setIcon(self, icon):
        """设置图标"""
        self._iconLabel.setPixmap(icon.pixmap(self._iconSize, self._iconSize))

    def setIconSize(self, size):
        """设置图标大小"""
        self._iconSize = size

    def enterEvent(self, ev, enterEv: QEnterEvent = None):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().enterEvent(ev)

    def mouseDoubleClickEvent(self, ev, mouseEv=None):
        super().mouseDoubleClickEvent(ev)
        self.maximized()

    def mousePressEvent(self, ev, mouseEv=None):
        if ev.button() == Qt.MouseButton.LeftButton:
            self._pos = ev.pos()
        ev.accept()

    def mouseReleaseEvent(self, ev, mouseEv=None):
        self._pos = None
        ev.accept()

    def mouseMoveEvent(self, event, mouseEv=None):
        if event.buttons() == Qt.MouseButton.LeftButton and self._pos:
            # 提交移动的坐标差
            self.windowMoved.emit(self.mapToGlobal(event.pos() - self._pos))
        event.accept()


class EFramelessWindow(EWindowResizable, EWindowMovable, QWidget):
    # 四周边距
    Margins = 5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = None
        self._titleBar = ETitleBar()

        self.InitialUi()
        self.setupSignal()

    def setupSignal(self):
        self._titleBar.WindowMinimized.connect(self.showMinimized)
        self._titleBar.windowMaximized.connect(self.showMaximized)
        self._titleBar.windowNormalized.connect(self.showNormal)
        self._titleBar.windowClosed.connect(self.close)
        self._titleBar.windowMoved.connect(self.move)
        self.windowTitleChanged.connect(self._titleBar.setTitle)
        self.windowIconChanged.connect(self._titleBar.setIcon)

    def InitialUi(self):

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        # 鼠标跟踪
        self.setMouseTracking(True)

        layout = QVBoxLayout(self)
        # 预留边界用于实现无边框窗口调整大小
        layout.setContentsMargins(
            self.Margins, self.Margins, self.Margins, self.Margins)

        self._titleBar = ETitleBar(self)
        layout.addWidget(self._titleBar)

    def setTitleBarHeight(self, height=38):
        self._titleBar.setHeight(height)

    def setIconSize(self, size):
        self._titleBar.setIconSize(size)

    def setWidget(self, widget):
        # 重复设置
        if self._widget == widget:
            return
        # 移除原widget
        if self.layout().count() > 1:
            self.layout().removeWidget(self._widget)

        self._widget = widget
        self._widget.setAutoFillBackground(True)

        self._widget.installEventFilter(self)
        size_policy = self._widget.sizePolicy()
        size_policy.setVerticalPolicy(QSizePolicy.Policy.Expanding)
        self._widget.setSizePolicy(size_policy)

        self.layout().addWidget(self._widget)

    def showMaximized(self):
        """最大化,要去除上下左右边界,如果不去除则边框地方会有空隙"""
        super().showMaximized()
        self.layout().setContentsMargins(0, 0, 0, 0)

    def showNormal(self):
        """还原,要保留上下左右边界,否则没有边框无法调整"""
        print("click 2")
        super().showNormal()
        self.layout().setContentsMargins(
            self.Margins, self.Margins,
            self.Margins, self.Margins)

    def eventFilter(self, obj, event):
        """事件过滤器,用于解决鼠标进入其它控件后还原为标准鼠标样式"""
        if isinstance(event, QEnterEvent):
            self.setCursor(Qt.CursorShape.ArrowCursor)
        return super().eventFilter(obj, event)

    def paintEvent(self, event, paintEv=None):
        """由于是全透明背景窗口,重绘事件中绘制透明度为1的难以发现的边框,用于调整窗口大小"""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(255, 255, 255, 1), 2 * self.Margins))
        painter.drawRect(self.rect())


from EPyQt.EWidgets import ETextEdit

if __name__ == "__main__":
    app = QApplication([])
    w = EFramelessWindow()
    w.setWidget(ETextEdit())
    w.show()
    app.exec()
