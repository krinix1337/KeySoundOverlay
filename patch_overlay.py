import re

with open('app/overlay_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

class_def_start = 'class KeyCap(QLabel):'
next_class_start = 'class OverlayWindow(QWidget):'

idx1 = code.find(class_def_start)
idx2 = code.find(next_class_start)

if idx1 != -1 and idx2 != -1:
    new_class = '''class KeyCap(QLabel):
    """Custom styled keycap widget that responds to press and release states."""
    def __init__(self, key_id, display_text, parent=None):
        super().__init__(display_text, parent)
        self.key_id = key_id
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(False)
        self.is_pressed = False
        self._scale = 1.0
        
        # Anim state
        self._anim_type = 'ripple'
        self._anim_val1 = 0
        self._anim_val2 = 0
        self._anim_timer = QTimer(self)
        self._anim_timer.setInterval(16)
        self._anim_timer.timeout.connect(self._step_anim)

    def trigger_anim(self):
        if not self._anim_type or self._anim_type == 'none':
            return
            
        if self._anim_type == 'ripple':
            self._anim_val1 = 0
            self._anim_val2 = max(self.width(), self.height()) * 1.2
            self._anim_alpha = 110
        elif self._anim_type == 'fade':
            self._anim_alpha = 200
        elif self._anim_type == 'bounce':
            self._anim_val1 = 8  # bounce offset
        self._anim_timer.start()

    def _step_anim(self):
        if self._anim_type == 'ripple':
            self._anim_val1 += max(3, int(self._anim_val2 * 0.09))
            self._anim_alpha = max(0, getattr(self, '_anim_alpha', 0) - 9)
            if self._anim_val1 >= self._anim_val2 or self._anim_alpha <= 0:
                self._anim_timer.stop()
                self._anim_alpha = 0
                self._anim_val1 = 0
        elif self._anim_type == 'fade':
            self._anim_alpha = max(0, getattr(self, '_anim_alpha', 0) - 15)
            if self._anim_alpha <= 0:
                self._anim_alpha = 0
                self._anim_timer.stop()
        elif self._anim_type == 'bounce':
            self._anim_val1 -= 1
            if self._anim_val1 <= 0:
                self._anim_val1 = 0
                self._anim_timer.stop()
        self.update()

    def paintEvent(self, event):
        if hasattr(self, '_anim_type') and self._anim_type == 'bounce' and getattr(self, '_anim_val1', 0) > 0:
            painter = QPainter(self)
            painter.translate(0, self._anim_val1)
            super().paintEvent(event)
            return

        super().paintEvent(event)
        
        if not hasattr(self, '_anim_alpha') or self._anim_alpha <= 0:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        if self._anim_type == 'ripple':
            cx, cy = self.width() // 2, self.height() // 2
            r = int(getattr(self, '_anim_val1', 0))
            if r <= 0: return
            gradient = QRadialGradient(cx, cy, r)
            gradient.setColorAt(0, QColor(255, 255, 255, self._anim_alpha))
            gradient.setColorAt(0.7, QColor(255, 255, 255, max(0, self._anim_alpha // 3)))
            gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(cx - r, cy - r, r * 2, r * 2)
        elif self._anim_type == 'fade':
            painter.setBrush(QColor(255, 255, 255, self._anim_alpha))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.rect())

    def update_style(self, theme_name, highlight_color, opacity=1.0, anim_type='ripple'):
        """Updates styling based on current state and theme."""
        if anim_type is True:
            anim_type = 'ripple'
        elif anim_type is False:
            anim_type = 'none'
        self._anim_type = anim_type
        style = get_overlay_key_qss(theme_name, highlight_color, self.is_pressed, opacity)
        font_size = int(11 * getattr(self, "_scale", 1.0))
        style += f"font-size: {font_size}px;"
        self.setStyleSheet(style)

'''
    code = code[:idx1] + new_class + code[idx2:]
    
    code = code.replace('widget.trigger_ripple()', 'widget.trigger_anim()')
    code = code.replace("hasattr(widget, 'trigger_ripple')", "hasattr(widget, 'trigger_anim')")
    
    with open('app/overlay_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('KeyCap animations updated')
else:
    print('Failed to find KeyCap class')
