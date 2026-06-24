import re

def patch():
    with open('app/settings_window.py', 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Imports
    if 'from app.icons import get_icon' not in code:
        code = code.replace('from app.utils import get_app_icon', 'from app.utils import get_app_icon\nfrom app.icons import get_icon')

    # 2. Translucent Background for windows
    if 'self.setAttribute(Qt.WA_TranslucentBackground, True)' not in code:
        code = code.replace('self.setWindowFlags(', 'self.setAttribute(Qt.WA_TranslucentBackground, True)\n        self.setWindowFlags(')

    # 3. Sidebar icons
    old_sb_btn = '''class SidebarButton(QPushButton):
    """Navigation button for the sidebar."""
    def __init__(self, emoji, text, parent=None):
        super().__init__(parent)
        self.setText(f"  {emoji}   {text}")'''
        
    new_sb_btn = '''class SidebarButton(QPushButton):
    """Navigation button for the sidebar."""
    def __init__(self, icon_name, text, parent=None):
        super().__init__(parent)
        self.setText(f" {text}")
        self.setIcon(get_icon(icon_name, color="#AAAAAA", size=24))
        self.setIconSize(QSize(20, 20))'''
    code = code.replace(old_sb_btn, new_sb_btn)

    # 4. Icon names for Nav buttons
    old_nav_items = '''        nav_items = [
            ("🔊", "Звук"),
            ("⌨️", "Оверлей"),
            ("🎨", "Внешний вид"),
            ("👤", "Профили"),
            ("⚙️", "Система"),
        ]'''
    new_nav_items = '''        nav_items = [
            ("sound", "Звук"),
            ("keyboard", "Оверлей"),
            ("palette", "Внешний вид"),
            ("profile", "Профили"),
            ("settings", "Система"),
        ]'''
    code = code.replace(old_nav_items, new_nav_items)
    
    # Nav hover fix to update icon color
    if 'self.setIcon(get_icon(icon_name' in code and 'def setChecked' not in code:
        # Actually it's easier to just use QIcon logic or let QSS handle it. 
        pass

    # 5. Section Labels
    code = code.replace('("🔊  Звук клавиш")', '("Звук клавиш")')
    code = code.replace('("⌨️  Оверлей клавиатуры")', '("Оверлей клавиатуры")')
    code = code.replace('("✨  Эффекты")', '("Эффекты")')
    code = code.replace('("🖱️  Оверлей мыши")', '("Оверлей мыши")')
    code = code.replace('("🎨  Внешний вид")', '("Внешний вид")')
    code = code.replace('("👤  Профили настроек")', '("Профили настроек")')
    code = code.replace('("⚙️  Система")', '("Система")')
    code = code.replace('("🔄  Обновления")', '("Обновления")')

    # 6. Buttons
    code = code.replace('("✔  Сохранить и закрыть")', '("Сохранить и закрыть")')
    code = code.replace('("▶  Тест звука")', '("Тест звука")')
    code = code.replace('("🔄  Сбросить позиции оверлеев")', '("Сбросить позиции оверлеев")')
    code = code.replace('("🎨  Создать кастомную тему…")', '("Создать кастомную тему…")')
    code = code.replace('("💾  Сохранить текущий")', '("Сохранить текущий")')
    code = code.replace('("📂  Загрузить")', '("Загрузить")')
    code = code.replace('("🗑️  Удалить")', '("Удалить")')
    code = code.replace('("🔍  Проверить обновления")', '("Проверить обновления")')
    code = code.replace('("⏳  Проверка…")', '("Проверка…")')
    code = code.replace('("⬆️  Установить обновление")', '("Установить обновление")')
    code = code.replace('("⚠️  Сбросить все настройки по умолчанию")', '("Сбросить все настройки по умолчанию")')

    # Add icons to buttons
    code = code.replace('self.btn_save = QPushButton("Сохранить и закрыть")', 'self.btn_save = QPushButton("Сохранить и закрыть")\n        self.btn_save.setIcon(get_icon("check", color="#FFFFFF"))')
    code = code.replace('self.btn_test = QPushButton("Тест звука")', 'self.btn_test = QPushButton("Тест звука")\n        self.btn_test.setIcon(get_icon("play", color="#FFFFFF"))')
    code = code.replace('self.btn_reset_pos = QPushButton("Сбросить позиции оверлеев")', 'self.btn_reset_pos = QPushButton("Сбросить позиции оверлеев")\n        self.btn_reset_pos.setIcon(get_icon("resize", color="#FFFFFF"))')
    code = code.replace('self.btn_create_theme = QPushButton("Создать кастомную тему…")', 'self.btn_create_theme = QPushButton("Создать кастомную тему…")\n        self.btn_create_theme.setIcon(get_icon("palette", color="#FFFFFF"))')
    code = code.replace('self.btn_profile_save = QPushButton("Сохранить текущий")', 'self.btn_profile_save = QPushButton("Сохранить текущий")\n        self.btn_profile_save.setIcon(get_icon("save", color="#FFFFFF"))')
    code = code.replace('self.btn_profile_load = QPushButton("Загрузить")', 'self.btn_profile_load = QPushButton("Загрузить")\n        self.btn_profile_load.setIcon(get_icon("load", color="#FFFFFF"))')
    code = code.replace('self.btn_profile_delete = QPushButton("Удалить")', 'self.btn_profile_delete = QPushButton("Удалить")\n        self.btn_profile_delete.setIcon(get_icon("trash", color="#FFFFFF"))')
    code = code.replace('self.btn_check_updates = QPushButton("Проверить обновления")', 'self.btn_check_updates = QPushButton("Проверить обновления")\n        self.btn_check_updates.setIcon(get_icon("search", color="#FFFFFF"))')
    code = code.replace('self.btn_install_update = QPushButton("Установить обновление")', 'self.btn_install_update = QPushButton("Установить обновление")\n        self.btn_install_update.setIcon(get_icon("update", color="#FFFFFF"))')
    code = code.replace('self.btn_reset_all = QPushButton("Сбросить все настройки по умолчанию")', 'self.btn_reset_all = QPushButton("Сбросить все настройки по умолчанию")\n        self.btn_reset_all.setIcon(get_icon("warning", color="#FFFFFF"))')

    # Profile list item
    code = code.replace('QListWidgetItem(f"  📄  {display}")', 'QListWidgetItem(f" {display}")\n            item.setIcon(get_icon("profile", color="#AAAAAA"))')
    
    with open('app/settings_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print('Settings patched successfully!')

patch()
