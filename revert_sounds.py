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
        self.combo_presets.addItem("   Cherry MX Brown (Тактильные)", "assets/cherry_mx_brown.wav")
        self.combo_presets.addItem("   Cherry MX Red (Линейные)", "assets/cherry_mx_red.wav")
        self.combo_presets.addItem("   Cherry MX Black (Тяжёлые линейные)", "assets/cherry_mx_black.wav")

        # --- Premium Switches ---
        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("⭐ PREMIUM SWITCHES", None)
        self.combo_presets.addItem("   Holy Panda (Thock)", "assets/holy_panda.wav")
        self.combo_presets.addItem("   Turquoise Tealio (Глубокий clack)", "assets/turquoise_tealio.wav")
        self.combo_presets.addItem("   NovelKeys Cream (Гладкие линейные)", "assets/nk_cream.wav")
        self.combo_presets.addItem("   Cream Travel (Тихие линейные)", "assets/cream_travel.wav")
        self.combo_presets.addItem("   EG Oreo (Тактильные)", "assets/eg_oreo.wav")
        self.combo_presets.addItem("   Crystal Purple (Звонкие)", "assets/crystal_purple.wav")
        self.combo_presets.addItem("   Topre Purple Hybrid (Тихие тактильные)", "assets/topre.wav")

        # --- 7 New Switches (Synthesized) ---
        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("✨ НОВЫЕ СВИЧИ", None)
        self.combo_presets.addItem("   Gateron Yellow (Ультра-тихий линейный)", "assets/gateron_yellow.wav")
        self.combo_presets.addItem("   Alps SKCM Orange (Винтажный тактильный)", "assets/alps_skcm.wav")
        self.combo_presets.addItem("   Kailh Box White (Box-клик)", "assets/kailh_box_white.wav")
        self.combo_presets.addItem("   Speed Silver (Быстрый линейный)", "assets/speed_silver.wav")
        self.combo_presets.addItem("   Topre 45g (Глубокий thock)", "assets/topre_45g.wav")
        self.combo_presets.addItem("   Boba U4 Silent (Беззвучный)", "assets/boba_u4.wav")
        self.combo_presets.addItem("   Akko CS Jelly Pink (Тактильный)", "assets/akko_jelly_pink.wav")

        self.combo_presets.insertSeparator(self.combo_presets.count())
        self.combo_presets.addItem("Другой звуковой файл...", "custom")'''

start_idx = code.find(start_str)
end_idx = code.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    code = code[:start_idx] + replacement + code[end_idx:]
    with open('app/settings_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Reverted combo_presets to old sounds successfully.')
else:
    print('Could not find replace block')
