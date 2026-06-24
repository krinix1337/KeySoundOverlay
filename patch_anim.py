import re

with open('app/settings_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add imports for animation
if 'QPropertyAnimation' not in code:
    code = code.replace('from PySide6.QtCore import Qt', 'from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve')
    code = code.replace('from PySide6.QtWidgets import (', 'from PySide6.QtWidgets import ( QGraphicsOpacityEffect,')

# Replace _switch_page
old_switch = '''    def _switch_page(self, idx):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)
        self.stack.setCurrentIndex(idx)'''

new_switch = '''    def _switch_page(self, idx):
        if self.stack.currentIndex() == idx:
            return
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == idx)
        
        # Fade animation
        self.effect = QGraphicsOpacityEffect(self.stack)
        self.stack.setGraphicsEffect(self.effect)
        self.anim = QPropertyAnimation(self.effect, b"opacity")
        self.anim.setDuration(150)
        self.anim.setStartValue(0.3)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.stack.setCurrentIndex(idx)
        self.anim.start()'''

if old_switch in code:
    code = code.replace(old_switch, new_switch)
    with open('app/settings_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Settings window animation added')
else:
    print('Could not find old switch page method')
