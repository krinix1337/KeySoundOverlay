import re

with open('app/settings_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('from PySide6.QtWidgets import (', 'from app.components import SettingToggle\nfrom PySide6.QtWidgets import (')

# Replace QCheckBox usage with SettingToggle for all typical settings
# General checkboxes
code = code.replace('self.chk_mouse_enabled = QCheckBox("Включить оверлей мыши")', 'self.chk_mouse_enabled = SettingToggle("Включить оверлей мыши")')
code = code.replace('self.chk_mouse_show_coords = QCheckBox("Показывать координаты")', 'self.chk_mouse_show_coords = SettingToggle("Показывать координаты")')
code = code.replace('self.chk_show_fullscreen = QCheckBox("Показывать оверлеи поверх полноэкранных приложений")', 'self.chk_show_fullscreen = SettingToggle("Показывать оверлеи поверх полноэкранных приложений")')
code = code.replace('self.chk_overlay_unlocked = QCheckBox("Разблокировать оверлей клавиатуры для перемещения")', 'self.chk_overlay_unlocked = SettingToggle("Разблокировать оверлей клавиатуры для перемещения")')
code = code.replace('self.chk_mouse_unlocked = QCheckBox("Разблокировать оверлей мыши для перемещения")', 'self.chk_mouse_unlocked = SettingToggle("Разблокировать оверлей мыши для перемещения")')

with open('app/settings_window.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Settings checkboxes upgraded to ToggleSwitches")
