# app/settings_window.py
import os
import json
import re
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, 
    QCheckBox, QLabel, QSlider, QPushButton, QComboBox, 
    QFileDialog, QGroupBox, QLineEdit, QMessageBox, QColorDialog,
    QScrollArea, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from app.themes import get_theme_qss, load_custom_themes, CUSTOM_THEMES
from app.utils import get_app_icon
from app.autostart import set_autostart, is_autostart_enabled
from app.update_manager import UpdateCheckerWorker, CURRENT_VERSION

class ColorSelectorButton(QPushButton):
    """Helper button that opens a color picker and shows the active color."""
    def __init__(self, initial_color, parent=None):
        super().__init__(parent)
        self.color = QColor(initial_color)
        self.setFixedWidth(80)
        self.update_style()
        self.clicked.connect(self.choose_color)

    def update_style(self):
        self.setStyleSheet(f"""
            background-color: {self.color.name()};
            border: 2px solid #555555;
            border-radius: 4px;
            min-height: 20px;
        """)

    def choose_color(self):
        color = QColorDialog.getColor(self.color, self, "Выберите цвет")
        if color.isValid():
            self.color = color
            self.update_style()


class ThemeCreatorDialog(QDialog):
    """Dialogue tool to build and export custom QSS stylesheets for settings and overlay."""
    def __init__(self, app_data_dir, theme_qss, parent=None):
        super().__init__(parent)
        self.app_data_dir = app_data_dir
        self.created_theme_id = ""
        self.setWindowTitle("Конструктор тем")
        self.setWindowIcon(get_app_icon())
        self.resize(400, 520)
        self.setStyleSheet(theme_qss)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(12)
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Название темы:"))
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Например: Space Blue")
        name_layout.addWidget(self.txt_name)
        self.layout.addLayout(name_layout)
        
        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background-color: transparent;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 5, 0)
        
        # Color Group 1: Settings Window
        grp_settings = QGroupBox("Цвета окон настроек")
        grp_settings_layout = QVBoxLayout(grp_settings)
        self.btn_win_bg = self.add_color_row(grp_settings_layout, "Фон окон:", "#1F1F1F")
        self.btn_win_text = self.add_color_row(grp_settings_layout, "Цвет текста:", "#FFFFFF")
        self.btn_win_accent = self.add_color_row(grp_settings_layout, "Акцентный цвет:", "#0078D4")
        self.btn_win_card = self.add_color_row(grp_settings_layout, "Фон карточек (табы/кнопки):", "#2D2D2D")
        self.btn_win_border = self.add_color_row(grp_settings_layout, "Цвет рамок:", "#3D3D3D")
        scroll_layout.addWidget(grp_settings)
        
        # Color Group 2: Keyboard/Mouse Overlay
        grp_overlay = QGroupBox("Цвета оверлея клавиш/мыши")
        grp_overlay_layout = QVBoxLayout(grp_overlay)
        self.btn_key_idle_bg = self.add_color_row(grp_overlay_layout, "Фон клавиш (простой):", "rgba(45, 45, 45, 180)")
        self.btn_key_idle_border = self.add_color_row(grp_overlay_layout, "Рамка клавиш (простой):", "rgba(62, 62, 62, 180)")
        self.btn_key_idle_text = self.add_color_row(grp_overlay_layout, "Текст клавиш (простой):", "#FFFFFF")
        
        self.btn_key_active_bg = self.add_color_row(grp_overlay_layout, "Фон клавиш (нажатие):", "#0078D4")
        self.btn_key_active_border = self.add_color_row(grp_overlay_layout, "Рамка клавиш (нажатие):", "#FFFFFF")
        self.btn_key_active_text = self.add_color_row(grp_overlay_layout, "Текст клавиш (нажатие):", "#FFFFFF")
        
        radius_layout = QHBoxLayout()
        radius_layout.addWidget(QLabel("Скругление углов клавиш:"))
        self.slider_radius = QSlider(Qt.Horizontal)
        self.slider_radius.setRange(0, 15)
        self.slider_radius.setValue(5)
        self.slider_radius.valueChanged.connect(lambda val: self.lbl_radius_val.setText(f"{val}px"))
        self.lbl_radius_val = QLabel("5px")
        self.lbl_radius_val.setFixedWidth(40)
        radius_layout.addWidget(self.slider_radius)
        radius_layout.addWidget(self.lbl_radius_val)
        grp_overlay_layout.addLayout(radius_layout)
        scroll_layout.addWidget(grp_overlay)
        
        scroll.setWidget(scroll_content)
        self.layout.addWidget(scroll)
        
        # Buttons
        bottom = QHBoxLayout()
        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.reject)
        self.btn_save = QPushButton("Сохранить тему")
        self.btn_save.clicked.connect(self.save_theme)
        self.btn_save.setDefault(True)
        
        bottom.addStretch()
        bottom.addWidget(btn_cancel)
        bottom.addWidget(self.btn_save)
        self.layout.addLayout(bottom)

    def add_color_row(self, layout, label_text, initial_color):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))
        btn = ColorSelectorButton(initial_color, self)
        row.addWidget(btn)
        layout.addLayout(row)
        return btn

    def save_theme(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите название темы.")
            return
            
        theme_id = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
        
        # Build theme dictionary
        theme_data = {
            "theme_display_name": name,
            "settings_window": {
                "background": self.btn_win_bg.color.name(),
                "text": self.btn_win_text.color.name(),
                "accent": self.btn_win_accent.color.name(),
                "card_bg": self.btn_win_card.color.name(),
                "border": self.btn_win_border.color.name()
            },
            "overlay": {
                "key_idle_bg": f"rgba({self.btn_key_idle_bg.color.red()}, {self.btn_key_idle_bg.color.green()}, {self.btn_key_idle_bg.color.blue()}, {self.btn_key_idle_bg.color.alpha()})",
                "key_idle_border": f"rgba({self.btn_key_idle_border.color.red()}, {self.btn_key_idle_border.color.green()}, {self.btn_key_idle_border.color.blue()}, {self.btn_key_idle_border.color.alpha()})",
                "key_idle_text": self.btn_key_idle_text.color.name(),
                "key_active_bg": self.btn_key_active_bg.color.name(),
                "key_active_border": self.btn_key_active_border.color.name(),
                "key_active_text": self.btn_key_active_text.color.name(),
                "key_radius": self.slider_radius.value(),
                "container_bg": f"rgba({self.btn_win_bg.color.red()}, {self.btn_win_bg.color.green()}, {self.btn_win_bg.color.blue()}, 120)",
                "container_border": self.btn_win_accent.color.name()
            }
        }
        
        themes_dir = os.path.join(self.app_data_dir, "themes")
        os.makedirs(themes_dir, exist_ok=True)
        path = os.path.join(themes_dir, f"{theme_id}.json")
        
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(theme_data, f, indent=4, ensure_ascii=False)
            self.created_theme_id = theme_id
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить тему:\n{str(e)}")


class SettingsWindow(QDialog):
    # Signals to notify changes to overlay and sound player
    settings_changed = Signal()
    reset_overlay_position_triggered = Signal()

    def __init__(self, config, sound_player):
        super().__init__()
        self.config = config
        self.sound_player = sound_player
        self.custom_themes_list = load_custom_themes(self.config.app_data_dir)
        
        self.setWindowTitle("KeySound Overlay - Настройки")
        self.setWindowIcon(get_app_icon())
        self.resize(500, 560)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowCloseButtonHint)
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)
        
        # Tab Widget
        self.tabs = QTabWidget(self)
        self.main_layout.addWidget(self.tabs)
        
        # Build Tabs
        self.build_sound_tab()
        self.build_overlay_tab()
        self.build_appearance_tab()
        self.build_system_tab()
        
        # Bottom Actions Layout
        bottom_layout = QHBoxLayout()
        self.btn_save = QPushButton("Сохранить и закрыть")
        self.btn_save.clicked.connect(self.save_and_close)
        
        self.btn_apply = QPushButton("Применить")
        self.btn_apply.clicked.connect(self.apply_settings)
        
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_apply)
        bottom_layout.addWidget(self.btn_save)
        self.main_layout.addLayout(bottom_layout)
        
        # Apply Styling and Load values
        self.load_values()
        self.apply_theme_styling()

    def apply_theme_styling(self):
        """Applies the QSS stylesheet matching the active configuration theme."""
        theme_name = self.config.get("theme")
        self.setStyleSheet(get_theme_qss(theme_name))

    def load_values(self):
        """Populates UI elements with values stored in settings config."""
        c = self.config
        
        # Sound Tab
        self.chk_sound_enabled.setChecked(c.get("sound_enabled"))
        self.txt_sound_path.setText(c.get("sound_file"))
        self.slider_volume.setValue(c.get("volume"))
        self.lbl_volume_val.setText(f"{c.get('volume')}%")
        self.chk_pitch_rand.setChecked(c.get("pitch_randomize"))
        self.chk_repeat_hold.setChecked(c.get("repeat_on_hold"))
        
        # Preset Switch Mapping
        sound_file = c.get("sound_file")
        preset_matched = False
        self.combo_presets.blockSignals(True)
        if not sound_file:
            self.combo_presets.setCurrentIndex(0)
            preset_matched = True
        else:
            for idx in range(self.combo_presets.count()):
                p_data = self.combo_presets.itemData(idx)
                if p_data and p_data != "custom":
                    normalized_file = sound_file.replace("\\", "/").lower()
                    normalized_preset = p_data.lower()
                    if normalized_file.endswith(normalized_preset):
                        self.combo_presets.setCurrentIndex(idx)
                        preset_matched = True
                        break
            if not preset_matched:
                self.combo_presets.setCurrentIndex(self.combo_presets.count() - 1)
        self.combo_presets.blockSignals(False)
        
        # Keyboard Overlay Tab
        self.chk_overlay_enabled.setChecked(c.get("overlay_enabled"))
        self.chk_overlay_unlocked.setChecked(c.get("overlay_unlocked"))
        kb_op = c.get("overlay_opacity")
        self.slider_opacity.setValue(int(kb_op * 100))
        self.lbl_opacity_val.setText(f"{int(kb_op * 100)}%")
        self.txt_custom_keys.setText(c.get("custom_layout_keys"))
        
        mode_idx = self.combo_mode.findData(c.get("overlay_mode"))
        if mode_idx >= 0:
            self.combo_mode.setCurrentIndex(mode_idx)
            
        self.toggle_custom_keys_visibility()
            
        color_idx = self.combo_color.findData(c.get("key_highlight_color"))
        if color_idx >= 0:
            self.combo_color.setCurrentIndex(color_idx)
            
        # Standalone Mouse Overlay Tab
        self.chk_mouse_enabled.setChecked(c.get("mouse_overlay_enabled"))
        self.chk_mouse_show_coords.setChecked(c.get("mouse_overlay_show_coords"))
        self.chk_mouse_show_clicks.setChecked(c.get("mouse_overlay_show_clicks"))
        self.chk_mouse_unlocked.setChecked(c.get("mouse_overlay_unlocked"))
        m_op = c.get("mouse_overlay_opacity")
        self.slider_mouse_opacity.setValue(int(m_op * 100))
        self.lbl_mouse_opacity_val.setText(f"{int(m_op * 100)}%")
        
        # Appearance Tab
        self.combo_theme.blockSignals(True)
        self.combo_theme.clear()
        self.combo_theme.addItem("Dark (Темная Fluent)", "dark")
        self.combo_theme.addItem("Light (Светлая Fluent)", "light")
        self.combo_theme.addItem("Glass (Полупрозрачное стекло)", "glass")
        self.combo_theme.addItem("Neon Blue (Киберпанк)", "neon")
        for display_name, theme_id in self.custom_themes_list:
            self.combo_theme.addItem(f"Кастомная: {display_name}", theme_id)
            
        theme_idx = self.combo_theme.findData(c.get("theme"))
        if theme_idx >= 0:
            self.combo_theme.setCurrentIndex(theme_idx)
        else:
            self.combo_theme.setCurrentIndex(0)
        self.combo_theme.blockSignals(False)
            
        # System Tab
        self.chk_autostart.setChecked(is_autostart_enabled())
        self.chk_minimize_tray.setChecked(c.get("minimize_to_tray"))
        self.chk_start_minimized.setChecked(c.get("start_minimized"))

    def preset_changed(self, index):
        """Called when a preset switch is selected in the combobox."""
        data = self.combo_presets.currentData()
        if data == "custom":
            pass
        elif data == "":
            self.txt_sound_path.setText("")
        else:
            from app.utils import get_resource_path
            self.txt_sound_path.setText(get_resource_path(data))

    def toggle_custom_keys_visibility(self):
        """Hides or shows custom keys text input depending on mode selection."""
        is_custom = (self.combo_mode.currentData() == "custom")
        self.lbl_custom_keys.setVisible(is_custom)
        self.txt_custom_keys.setVisible(is_custom)

    def apply_settings(self):
        """Saves current GUI adjustments into configuration and triggers reloads."""
        c = self.config
        
        # Sound Configuration
        c.set("sound_enabled", self.chk_sound_enabled.isChecked())
        c.set("sound_file", self.txt_sound_path.text())
        c.set("volume", self.slider_volume.value())
        c.set("pitch_randomize", self.chk_pitch_rand.isChecked())
        c.set("repeat_on_hold", self.chk_repeat_hold.isChecked())
        
        # Keyboard Overlay Configuration
        c.set("overlay_enabled", self.chk_overlay_enabled.isChecked())
        c.set("overlay_unlocked", self.chk_overlay_unlocked.isChecked())
        c.set("overlay_opacity", self.slider_opacity.value() / 100.0)
        c.set("overlay_mode", self.combo_mode.currentData())
        c.set("key_highlight_color", self.combo_color.currentData())
        c.set("custom_layout_keys", self.txt_custom_keys.text())
        
        # Standalone Mouse Overlay Configuration
        c.set("mouse_overlay_enabled", self.chk_mouse_enabled.isChecked())
        c.set("mouse_overlay_show_coords", self.chk_mouse_show_coords.isChecked())
        c.set("mouse_overlay_show_clicks", self.chk_mouse_show_clicks.isChecked())
        c.set("mouse_overlay_unlocked", self.chk_mouse_unlocked.isChecked())
        c.set("mouse_overlay_opacity", self.slider_mouse_opacity.value() / 100.0)
        
        # Appearance Configuration
        c.set("theme", self.combo_theme.currentData())
        
        # System Configuration
        c.set("minimize_to_tray", self.chk_minimize_tray.isChecked())
        c.set("start_minimized", self.chk_start_minimized.isChecked())
        
        # Autostart registry handler
        autostart_request = self.chk_autostart.isChecked()
        if autostart_request != is_autostart_enabled():
            set_autostart(autostart_request)
            
        c.save()
        
        # Update components
        self.sound_player.reload()
        self.apply_theme_styling()
        self.settings_changed.emit()

    def save_and_close(self):
        self.apply_settings()
        self.accept()

    def reset_settings(self):
        """Resets all options to default values."""
        reply = QMessageBox.question(
            self, "Сброс настроек", 
            "Вы действительно хотите сбросить все настройки приложения на значения по умолчанию?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.config.reset()
            self.load_values()
            self.apply_settings()
            QMessageBox.information(self, "Готово", "Настройки сброшены!")

    def check_for_updates_clicked(self):
        self.btn_check_updates.setEnabled(False)
        self.btn_check_updates.setText("Проверка...")
        
        self.update_checker_worker = UpdateCheckerWorker()
        self.update_checker_worker.check_finished.connect(self.on_settings_update_checked)
        self.update_checker_worker.check_failed.connect(self.on_settings_update_failed)
        self.update_checker_worker.start()

    def on_settings_update_checked(self, update_available, latest_version, changelog, download_url):
        self.btn_check_updates.setEnabled(True)
        self.btn_check_updates.setText("Проверить обновления")
        
        if update_available:
            self.latest_version = latest_version
            self.changelog = changelog
            self.download_url = download_url
            self.btn_install_update.setVisible(True)
            self.lbl_app_version.setText(f"Версия приложения: {CURRENT_VERSION} (Доступно обновление: {latest_version}!)")
            
            # Automatically trigger update dialog
            self.run_update_dialog()
        else:
            self.btn_install_update.setVisible(False)
            self.lbl_app_version.setText(f"Версия приложения: {CURRENT_VERSION} (У вас последняя версия)")
            QMessageBox.information(self, "Обновление", "У вас установлена последняя версия программы!")

    def on_settings_update_failed(self, error_msg):
        self.btn_check_updates.setEnabled(True)
        self.btn_check_updates.setText("Проверить обновления")
        QMessageBox.warning(self, "Ошибка обновления", f"Не удалось проверить обновления:\n{error_msg}")

    def run_update_dialog(self):
        if hasattr(self, 'latest_version') and self.download_url:
            from app.update_dialog import UpdateDialog
            update_dlg = UpdateDialog(self.config, self)
            update_dlg.set_update_info(self.latest_version, self.changelog, self.download_url)
            update_dlg.exec()

    # TAB UI CONSTRUCTORS
    def build_sound_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        self.chk_sound_enabled = QCheckBox("Включить воспроизведение звуков")
        layout.addWidget(self.chk_sound_enabled)
        
        grp_file = QGroupBox("Файл звука")
        grp_file_layout = QVBoxLayout(grp_file)
        
        preset_layout = QHBoxLayout()
        preset_layout.addWidget(QLabel("Предустановленные свичи:"))
        self.combo_presets = QComboBox()
        self.combo_presets.addItem("По умолчанию (встроенный клик)", "")
        self.combo_presets.addItem("Cherry MX Blue (Кликающие)", "assets/cherry_mx_blue.wav")
        self.combo_presets.addItem("Cherry MX Brown (Тактильные)", "assets/cherry_mx_brown.wav")
        self.combo_presets.addItem("Cherry MX Red (Линейные)", "assets/cherry_mx_red.wav")
        self.combo_presets.addItem("Cherry MX Black (Тяжелые линейные)", "assets/cherry_mx_black.wav")
        self.combo_presets.addItem("Holy Panda (Популярный Thock)", "assets/holy_panda.wav")
        self.combo_presets.addItem("Turquoise Tealio (Глубокий clack)", "assets/turquoise_tealio.wav")
        self.combo_presets.addItem("NovelKeys Cream (Гладкие линейные)", "assets/nk_cream.wav")
        self.combo_presets.addItem("Cream Travel (Тихие линейные)", "assets/cream_travel.wav")
        self.combo_presets.addItem("EG Oreo (Тактильные)", "assets/eg_oreo.wav")
        self.combo_presets.addItem("Crystal Purple (Звонкие WAV)", "assets/crystal_purple.wav")
        self.combo_presets.addItem("Topre Purple Hybrid (Тихие тактильные)", "assets/topre.wav")
        self.combo_presets.addItem("Другой звуковой файл...", "custom")
        preset_layout.addWidget(self.combo_presets)
        grp_file_layout.addLayout(preset_layout)
        
        self.combo_presets.currentIndexChanged.connect(self.preset_changed)
        
        file_input_layout = QHBoxLayout()
        self.txt_sound_path = QLineEdit()
        self.txt_sound_path.setPlaceholderText("По умолчанию (встроенный клик)")
        self.btn_browse = QPushButton("Обзор...")
        self.btn_browse.clicked.connect(self.browse_sound_file)
        
        file_input_layout.addWidget(self.txt_sound_path)
        file_input_layout.addWidget(self.btn_browse)
        grp_file_layout.addLayout(file_input_layout)
        
        self.btn_test = QPushButton("🔊 Протестировать звук")
        self.btn_test.clicked.connect(self.test_sound_file)
        grp_file_layout.addWidget(self.btn_test)
        
        layout.addWidget(grp_file)
        
        grp_params = QGroupBox("Параметры звука")
        grp_params_layout = QVBoxLayout(grp_params)
        
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Громкость:"))
        self.slider_volume = QSlider(Qt.Horizontal)
        self.slider_volume.setRange(0, 100)
        self.slider_volume.valueChanged.connect(lambda val: self.lbl_volume_val.setText(f"{val}%"))
        self.lbl_volume_val = QLabel("80%")
        self.lbl_volume_val.setFixedWidth(40)
        vol_layout.addWidget(self.slider_volume)
        vol_layout.addWidget(self.lbl_volume_val)
        grp_params_layout.addLayout(vol_layout)
        
        self.chk_pitch_rand = QCheckBox("Живой звук (случайный Pitch и громкость)")
        self.chk_repeat_hold = QCheckBox("Повторять звук при удержании клавиши")
        grp_params_layout.addWidget(self.chk_pitch_rand)
        grp_params_layout.addWidget(self.chk_repeat_hold)
        
        layout.addWidget(grp_params)
        layout.addStretch()
        self.tabs.addTab(tab, "Звук")

    def build_overlay_tab(self):
        tab = QWidget()
        main_layout = QVBoxLayout(tab)
        main_layout.setSpacing(10)
        
        # Keyboard Overlay settings group
        grp_key = QGroupBox("Оверлей Клавиатуры")
        key_layout = QVBoxLayout(grp_key)
        
        self.chk_overlay_enabled = QCheckBox("Отображать оверлей клавиатуры")
        self.chk_overlay_unlocked = QCheckBox("Разблокировать перемещение клавиатуры (перетаскивание)")
        key_layout.addWidget(self.chk_overlay_enabled)
        key_layout.addWidget(self.chk_overlay_unlocked)
        
        op_layout = QHBoxLayout()
        op_layout.addWidget(QLabel("Прозрачность клавиатуры:"))
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(0, 100)
        self.slider_opacity.valueChanged.connect(lambda val: self.lbl_opacity_val.setText(f"{val}%"))
        self.lbl_opacity_val = QLabel("85%")
        self.lbl_opacity_val.setFixedWidth(40)
        op_layout.addWidget(self.slider_opacity)
        op_layout.addWidget(self.lbl_opacity_val)
        key_layout.addLayout(op_layout)
        
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Режим отображения:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Полная клавиатура", "full")
        self.combo_mode.addItem("Игровой (WASD + Space + Modifiers)", "wasd")
        self.combo_mode.addItem("Кликер Osu! (Z + X + Space + Esc)", "osu")
        self.combo_mode.addItem("Dota 2 (Панель клавиш)", "dota")
        self.combo_mode.addItem("Своя раскладка (Кастомная)", "custom")
        self.combo_mode.addItem("Только нажатые клавиши (лог)", "pressed")
        mode_layout.addWidget(self.combo_mode)
        key_layout.addLayout(mode_layout)
        
        self.custom_keys_layout = QHBoxLayout()
        self.lbl_custom_keys = QLabel("Клавиши раскладки (через запятую):")
        self.txt_custom_keys = QLineEdit()
        self.txt_custom_keys.setToolTip("Введите клавиши, например: q, w, e, r, d, f, space")
        self.custom_keys_layout.addWidget(self.lbl_custom_keys)
        self.custom_keys_layout.addWidget(self.txt_custom_keys)
        key_layout.addLayout(self.custom_keys_layout)
        
        self.combo_mode.currentIndexChanged.connect(self.toggle_custom_keys_visibility)
        
        color_layout = QHBoxLayout()
        color_layout.addWidget(QLabel("Цвет подсветки клавиш:"))
        self.combo_color = QComboBox()
        self.combo_color.addItem("Windows Blue (Accent)", "#0078D4")
        self.combo_color.addItem("Neon Cyan", "#00F0FF")
        self.combo_color.addItem("Cyber Pink", "#FF007F")
        self.combo_color.addItem("Acid Green", "#10B981")
        self.combo_color.addItem("Vivid Purple", "#B400FF")
        self.combo_color.addItem("Sunset Orange", "#FF5722")
        color_layout.addWidget(self.combo_color)
        key_layout.addLayout(color_layout)
        
        main_layout.addWidget(grp_key)
        
        # Standalone Mouse Overlay settings group
        grp_mouse = QGroupBox("Оверлей Мыши (Мышка)")
        mouse_layout_v = QVBoxLayout(grp_mouse)
        
        self.chk_mouse_enabled = QCheckBox("Отображать оверлей мыши")
        self.chk_mouse_show_coords = QCheckBox("Показывать координаты мыши (X / Y)")
        self.chk_mouse_show_clicks = QCheckBox("Подсвечивать клики кнопок")
        self.chk_mouse_unlocked = QCheckBox("Разблокировать перемещение оверлея мыши")
        
        mouse_layout_v.addWidget(self.chk_mouse_enabled)
        mouse_layout_v.addWidget(self.chk_mouse_show_coords)
        mouse_layout_v.addWidget(self.chk_mouse_show_clicks)
        mouse_layout_v.addWidget(self.chk_mouse_unlocked)
        
        m_op_layout = QHBoxLayout()
        m_op_layout.addWidget(QLabel("Прозрачность оверлея мыши:"))
        self.slider_mouse_opacity = QSlider(Qt.Horizontal)
        self.slider_mouse_opacity.setRange(0, 100)
        self.slider_mouse_opacity.valueChanged.connect(lambda val: self.lbl_mouse_opacity_val.setText(f"{val}%"))
        self.lbl_mouse_opacity_val = QLabel("85%")
        self.lbl_mouse_opacity_val.setFixedWidth(40)
        m_op_layout.addWidget(self.slider_mouse_opacity)
        m_op_layout.addWidget(self.lbl_mouse_opacity_val)
        mouse_layout_v.addLayout(m_op_layout)
        
        main_layout.addWidget(grp_mouse)
        
        # Reset position button
        self.btn_reset_pos = QPushButton("🔄 Сбросить позиции оверлеев")
        self.btn_reset_pos.clicked.connect(self.reset_overlay_position_triggered.emit)
        main_layout.addWidget(self.btn_reset_pos)
        
        main_layout.addStretch()
        self.tabs.addTab(tab, "Оверлей")

    def build_appearance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        grp_theme = QGroupBox("Тема оформления приложения")
        grp_theme_layout = QVBoxLayout(grp_theme)
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Тема:"))
        self.combo_theme = QComboBox()
        theme_layout.addWidget(self.combo_theme)
        grp_theme_layout.addLayout(theme_layout)
        
        # Theme creator button
        self.btn_create_theme = QPushButton("🎨 Создать кастомную тему...")
        self.btn_create_theme.clicked.connect(self.open_theme_creator)
        grp_theme_layout.addWidget(self.btn_create_theme)
        
        layout.addWidget(grp_theme)
        layout.addStretch()
        self.tabs.addTab(tab, "Внешний вид")

    def build_system_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        grp_sys = QGroupBox("Настройки системы")
        grp_sys_layout = QVBoxLayout(grp_sys)
        
        self.chk_autostart = QCheckBox("Запускать вместе с Windows (Registry)")
        self.chk_minimize_tray = QCheckBox("Сворачивать в трей при закрытии окон")
        self.chk_start_minimized = QCheckBox("Запускать скрытым (только в трее)")
        
        grp_sys_layout.addWidget(self.chk_autostart)
        grp_sys_layout.addWidget(self.chk_minimize_tray)
        grp_sys_layout.addWidget(self.chk_start_minimized)
        
        layout.addWidget(grp_sys)
        
        grp_update = QGroupBox("Обновление программы")
        grp_update_layout = QVBoxLayout(grp_update)
        
        self.lbl_app_version = QLabel(f"Версия приложения: {CURRENT_VERSION}")
        grp_update_layout.addWidget(self.lbl_app_version)
        
        update_btn_layout = QHBoxLayout()
        self.btn_check_updates = QPushButton("Проверить обновления")
        self.btn_check_updates.clicked.connect(self.check_for_updates_clicked)
        self.btn_install_update = QPushButton("Обновить")
        self.btn_install_update.setStyleSheet("background-color: #10B981; color: white; font-weight: bold;")
        self.btn_install_update.setVisible(False)
        self.btn_install_update.clicked.connect(self.run_update_dialog)
        
        update_btn_layout.addWidget(self.btn_check_updates)
        update_btn_layout.addWidget(self.btn_install_update)
        grp_update_layout.addLayout(update_btn_layout)
        
        layout.addWidget(grp_update)
        
        self.btn_reset_all = QPushButton("⚠️ Сбросить настройки по умолчанию")
        self.btn_reset_all.clicked.connect(self.reset_settings)
        layout.addWidget(self.btn_reset_all)
        
        lbl_privacy_title = QLabel("Безопасность и конфиденциальность:")
        lbl_privacy_title.setStyleSheet("font-weight: bold; margin-top: 10px; color: #888888;")
        layout.addWidget(lbl_privacy_title)
        
        lbl_privacy = QLabel(
            "Приложение использует глобальный hook исключительно для "
            "отображения подсветки клавиатуры/мыши и воспроизведения звуков кликов. "
            "Никакие вводимые данные или перемещения мыши не сохраняются и не отправляются в сеть."
        )
        lbl_privacy.setWordWrap(True)
        lbl_privacy.setStyleSheet("font-size: 11px; color: #888888; font-style: italic; line-height: 14px;")
        layout.addWidget(lbl_privacy)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Настройка")

    # FILE BROWSING / DIALOGS
    def browse_sound_file(self):
        file_filter = "Звуковые файлы (*.wav *.mp3 *.ogg);;WAV (*.wav);;MP3 (*.mp3);;OGG (*.ogg)"
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл звука", "", file_filter)
        if file_path:
            self.txt_sound_path.setText(file_path)
            custom_idx = self.combo_presets.findData("custom")
            if custom_idx >= 0:
                self.combo_presets.setCurrentIndex(custom_idx)

    def test_sound_file(self):
        file_path = self.txt_sound_path.text()
        volume = self.slider_volume.value()
        self.sound_player.test_play(file_path, volume)
        
    def open_theme_creator(self):
        """Opens ThemeCreatorDialog to build a custom color theme."""
        dialog = ThemeCreatorDialog(self.config.app_data_dir, get_theme_qss(self.config.get("theme")), self)
        if dialog.exec():
            # Reload themes list and select the new custom theme
            self.custom_themes_list = load_custom_themes(self.config.app_data_dir)
            self.load_values()
            
            created_id = dialog.created_theme_id
            self.config.set("theme", created_id)
            self.apply_theme_styling()
            self.settings_changed.emit()

    def reject(self):
        self.hide()
