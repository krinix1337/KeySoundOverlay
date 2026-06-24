import re

with open('app/settings_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

start_str = 'self.combo_presets.addItem("По умолчанию (встроенный клик)", "")'
end_str = 'self.combo_presets.addItem("Другой звуковой файл...", "custom")'

replacement = '''self.combo_presets.addItem("По умолчанию (встроенный клик)", "")

        # --- Cherry MX ---
        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("🍒 CHERRY MX", None)
        
        self.combo_presets.addItem("   Cherry MX Blue (Кликающие)", "assets/cherry_mx_blue.wav")
        self.combo_presets.addItem("   Cherry MX Brown (Тактильные)", "assets/cherry_mx_brown_abs.ogg")
        self.combo_presets.addItem("   Cherry MX Red (Линейные)", "assets/cherry_mx_red_abs.ogg")
        self.combo_presets.addItem("   Cherry MX Black (Тяжёлые линейные)", "assets/cherry_mx_black_abs.ogg")

        # --- Premium Switches ---
        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("⭐ PREMIUM SWITCHES", None)
        self.combo_presets.addItem("   Glorious Panda (Thock)", "assets/glorious_panda.ogg")
        self.combo_presets.addItem("   Tealios V2 (Smooth Linear)", "assets/tealios_v2.wav")
        self.combo_presets.addItem("   NovelKeys Cream (Linear)", "assets/nk_cream.wav")
        self.combo_presets.addItem("   Kailh Box White (Box-клик)", "assets/kailh_box_white.mp3")

        # --- Vintage & Others ---
        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("🕰️ VINTAGE & OTHER", None)
        self.combo_presets.addItem("   Alps SKCM Orange (Винтажные)", "assets/alps_skcm.wav")
        self.combo_presets.addItem("   Topre 45g (Низкий thock)", "assets/topre_45g.wav")
        self.combo_presets.addItem("   Unicomp Classic (Buckling Spring)", "assets/unicomp_classic.ogg")
        self.combo_presets.addItem("   Boba U4 Silent (Бесшумные)", "assets/boba_u4.wav")
        self.combo_presets.addItem("   Akko CS Jelly Pink (Линейные)", "assets/akko_jelly_pink.wav")

        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("Другой звуковой файл...", "custom")
        
        # Disable category headers
        model = self.combo_presets.model()
        for i in range(self.combo_presets.count()):
            if self.combo_presets.itemData(i) is None:
                item = model.item(i)
                if item:
                    item.setEnabled(False)'''

start_idx = code.find(start_str)
end_idx = code.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + replacement + code[end_idx:]
    with open('app/settings_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Replaced combo_presets logic successfully.')
else:
    print('Failed to find replace block.')

# Update animations combo
anim_start = 'self.combo_anim.addItem("Рябь (Ripple)", "ripple")'
if anim_start in code:
    anim_replace = '''self.combo_anim.addItem("Рябь (Ripple)", "ripple")
        self.combo_anim.addItem("Затухание (Fade)", "fade")
        self.combo_anim.addItem("Прыжок (Bounce)", "bounce")'''
    code = code.replace(anim_start, anim_replace)
    with open('app/settings_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Animations updated')

