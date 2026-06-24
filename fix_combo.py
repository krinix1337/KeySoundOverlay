import re

with open('app/settings_window.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if 'self.chk_key_anim = QCheckBox' in line:
        new_lines.append('        self.combo_anim = QComboBox()\n')
        new_lines.append('        self.combo_anim.addItem("Рябь (Ripple)", "ripple")\n')
        new_lines.append('        self.combo_anim.addItem("Затухание (Fade)", "fade")\n')
        new_lines.append('        self.combo_anim.addItem("Прыжок (Bounce)", "bounce")\n')
        new_lines.append('        self.combo_anim.addItem("Без анимации", "none")\n')
    else:
        new_lines.append(line)

with open('app/settings_window.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Fixed combo_anim definition')
