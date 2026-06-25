from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox
from PySide6.QtGui import QPainter, QColor, QPainterPath
from PySide6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve, Property

class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 24)
        self.setCursor(Qt.PointingHandCursor)
        self._thumb_x = 2
        self.anim = QPropertyAnimation(self, b"thumb_x")
        self.anim.setDuration(120)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.toggled.connect(self._start_anim)
        self.setStyleSheet("background: transparent;")

    def _start_anim(self, checked):
        self.anim.setStartValue(self._thumb_x)
        self.anim.setEndValue(20 if checked else 2)
        self.anim.start()

    @Property(float)
    def thumb_x(self): return self._thumb_x

    @thumb_x.setter
    def thumb_x(self, val):
        self._thumb_x = val
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        rect = QRect(0, 0, self.width(), self.height())
        if self.isChecked():
            p.setBrush(QColor("#0078D7")) # Accent color
        else:
            p.setBrush(QColor(128, 128, 128, 100)) # Universal Off background
        p.drawRoundedRect(rect, 12, 12)
        
        p.setBrush(Qt.white)
        p.drawEllipse(int(self._thumb_x), 2, 20, 20)
        p.end()

class SettingToggle(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        l = QHBoxLayout(self)
        l.setContentsMargins(4, 4, 4, 4)
        self.lbl = QLabel(text)
        self.lbl.setStyleSheet("font-size: 14px;")
        self.switch = ToggleSwitch()
        l.addWidget(self.lbl)
        l.addStretch()
        l.addWidget(self.switch)
        
    def isChecked(self):
        return self.switch.isChecked()
        
    def setChecked(self, v):
        self.switch.setChecked(v)
        self.switch.thumb_x = 20 if v else 2
