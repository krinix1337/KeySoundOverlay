# app/snap_guides.py
import ctypes
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor

class SnapGuideOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        
        # Cover all screens
        try:
            user32 = ctypes.windll.user32
            w = user32.GetSystemMetrics(78) # SM_CXVIRTUALSCREEN
            h = user32.GetSystemMetrics(79) # SM_CYVIRTUALSCREEN
            x = user32.GetSystemMetrics(76) # SM_XVIRTUALSCREEN
            y = user32.GetSystemMetrics(77) # SM_YVIRTUALSCREEN
            self.setGeometry(x, y, w, h)
        except Exception:
            from PySide6.QtWidgets import QApplication
            screen = QApplication.primaryScreen().geometry()
            self.setGeometry(screen)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        
        pen = QPen(QColor(0, 240, 255, 180), 1)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        
        # Draw crosshair at the exact center of the primary screen
        from PySide6.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        cx = screen.x() + screen.width() // 2 - self.x()
        cy = screen.y() + screen.height() // 2 - self.y()
        
        # Vertical line
        painter.drawLine(cx, 0, cx, self.height())
        # Horizontal line
        painter.drawLine(0, cy, self.width(), cy)
        
        # Draw a small center circle
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(cx - 10, cy - 10, 20, 20)
