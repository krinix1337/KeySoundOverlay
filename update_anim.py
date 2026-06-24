import re

with open('app/settings_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace chk_key_anim with combo_anim
code = code.replace('self.chk_key_anim = QCheckBox("Включить анимацию нажатия (ripple-эффект)")', 
'''self.combo_anim = QComboBox()
        self.combo_anim.addItem("Рябь (Ripple)", "ripple")
        self.combo_anim.addItem("Затухание (Fade)", "fade")
        self.combo_anim.addItem("Прыжок (Bounce)", "bounce")
        self.combo_anim.addItem("Без анимации", "none")''')

code = code.replace('fx_l.addWidget(self.chk_key_anim)', 
'''fx_l.addWidget(QLabel("Анимация нажатия:"))
        fx_l.addWidget(self.combo_anim)''')

code = code.replace('self.chk_key_anim.setChecked(c.get("key_press_animation"))', 
'''anim_val = c.get("key_press_animation", "ripple")
        if anim_val is True: anim_val = "ripple"
        if anim_val is False: anim_val = "none"
        idx = self.combo_anim.findData(anim_val)
        if idx >= 0: self.combo_anim.setCurrentIndex(idx)''')

code = code.replace('c.set("key_press_animation", self.chk_key_anim.isChecked())', 
'c.set("key_press_animation", self.combo_anim.currentData())')

with open('app/settings_window.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated settings_window.py combo_anim')
