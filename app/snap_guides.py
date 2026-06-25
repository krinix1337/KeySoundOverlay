# app/snap_guides.py
import ctypes
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QPainter, QPen, QColor


class SnapGuideOverlay(QWidget):
    SNAP_THRESHOLD = 20

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint |
            Qt.Tool | Qt.WindowTransparentForInput
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self._active_snaps = set()
        self._screen_rect = QRect()
        try:
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(78)
            h = user32.GetSystemMetrics(79)
            x = user32.GetSystemMetrics(76)
            y = user32.GetSystemMetrics(77)
            self.setGeometry(x, y, w, h)
        except Exception:
            screen = QApplication.primaryScreen().geometry()
            self.setGeometry(screen)

    def update_snap_state(self, overlay_rect):
        screen = QApplication.screenAt(overlay_rect.center())
        if screen is None:
            screen = QApplication.primaryScreen()
        sr = screen.geometry()
        self._screen_rect = sr
        self._active_snaps.clear()
        scx = sr.x() + sr.width() // 2
        scy = sr.y() + sr.height() // 2
        ocx = overlay_rect.x() + overlay_rect.width() // 2
        ocy = overlay_rect.y() + overlay_rect.height() // 2
        t = self.SNAP_THRESHOLD
        if abs(ocx - scx) < t:
            self._active_snaps.add('cx')
        if abs(ocy - scy) < t:
            self._active_snaps.add('cy')
        if abs(overlay_rect.left() - sr.left()) < t:
            self._active_snaps.add('left')
        if abs(overlay_rect.right() - sr.right()) < t:
            self._active_snaps.add('right')
        if abs(overlay_rect.top() - sr.top()) < t:
            self._active_snaps.add('top')
        if abs(overlay_rect.bottom() - sr.bottom()) < t:
            self._active_snaps.add('bottom')
        self.update()

    def get_snapped_position(self, overlay_rect):
        screen = QApplication.screenAt(overlay_rect.center())
        if screen is None:
            screen = QApplication.primaryScreen()
        sr = screen.geometry()
        x = overlay_rect.x()
        y = overlay_rect.y()
        ow = overlay_rect.width()
        oh = overlay_rect.height()
        t = self.SNAP_THRESHOLD
        scx = sr.x() + sr.width() // 2
        scy = sr.y() + sr.height() // 2
        ocx = x + ow // 2
        ocy = y + oh // 2
        if abs(ocx - scx) < t:
            x = scx - ow // 2
        if abs(ocy - scy) < t:
            y = scy - oh // 2
        if abs(x - sr.left()) < t:
            x = sr.left()
        elif abs((x + ow) - sr.right()) < t:
            x = sr.right() - ow
        if abs(y - sr.top()) < t:
            y = sr.top()
        elif abs((y + oh) - sr.bottom()) < t:
            y = sr.bottom() - oh
        return x, y

    def paintEvent(self, event):
        if not self._screen_rect.isValid():
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        sr = self._screen_rect
        dim_pen = QPen(QColor(100, 100, 100, 60), 1, Qt.DashLine)
        active_pen = QPen(QColor(0, 200, 255, 200), 1, Qt.SolidLine)
        ox, oy = self.x(), self.y()
        cx = sr.x() + sr.width() // 2 - ox
        cy = sr.y() + sr.height() // 2 - oy
        left = sr.left() - ox
        right = sr.right() - ox
        top = sr.top() - oy
        bottom = sr.bottom() - oy
        painter.setPen(active_pen if 'cx' in self._active_snaps else dim_pen)
        painter.drawLine(cx, top, cx, bottom)
        painter.setPen(active_pen if 'cy' in self._active_snaps else dim_pen)
        painter.drawLine(left, cy, right, cy)
        painter.setPen(active_pen if 'left' in self._active_snaps else dim_pen)
        painter.drawLine(left, top, left, bottom)
        painter.setPen(active_pen if 'right' in self._active_snaps else dim_pen)
        painter.drawLine(right, top, right, bottom)
        painter.setPen(active_pen if 'top' in self._active_snaps else dim_pen)
        painter.drawLine(left, top, right, top)
        painter.setPen(active_pen if 'bottom' in self._active_snaps else dim_pen)
        painter.drawLine(left, bottom, right, bottom)
        if 'cx' in self._active_snaps or 'cy' in self._active_snaps:
            painter.setPen(active_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(cx - 8, cy - 8, 16, 16)
