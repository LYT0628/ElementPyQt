from enum import Enum, auto


class WindowState(Enum):
    # ´°¿Ú×´Ì¬»ú#
    Maximum = auto()
    Normal = auto()
    Minimum = auto()


class Edge(Enum):
    LEFT = auto()
    TOP = auto()
    RIGHT = auto()
    BOTTOM = auto()
    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    RIGHT_BOTTOM = auto()
    LEFT_BOTTOM = auto()


