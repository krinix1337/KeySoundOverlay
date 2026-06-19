# app/settings_window.py
import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget, 
    QCheckBox, QLabel, QSlider, QPushButton, QComboBox, 
    QFileDialog, QGroupBox, QLineEdit, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont
from app.themes import get_theme_qss
from app.utils import get_app_icon
from app.autostart import set_autostart, is_autostart_enabled

class SettingsWindow(QDialog):
    # Signals to notify changes to overlay and sound player
    settings_changed = Signal()
    reset_overlay_position_triggered = Signal()

    def __init__(self, config, sound_player):
        super().__init__()
        self.config = config
        self.sound_player = sound_player
        
        self.setWindowTitle("KeySound Overlay - Настройки")
        self.setWindowIcon(get_app_icon())
        self.resize(480, 520)
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
        
        # Overlay Tab
        self.chk_overlay_enabled.setChecked(c.get("overlay_enabled"))
        self.chk_overlay_unlocked.setChecked(c.get("overlay_unlocked"))
        self.slider_opacity.setValue(int(c.get("overlay_opacity") * 100))
        self.lbl_opacity_val.setText(f"{int(c.get('overlay_opacity') * 100)}%")
        
        self.txt_custom_keys.setText(c.get("custom_layout_keys"))
        
        mode_idx = self.combo_mode.findData(c.get("overlay_mode"))
        if mode_idx >= 0:
            self.combo_mode.setCurrentIndex(mode_idx)
            
        self.toggle_custom_keys_visibility()
            
        color_idx = self.combo_color.findData(c.get("key_highlight_color"))
        if color_idx >= 0:
            self.combo_color.setCurrentIndex(color_idx)
            
        # Appearance Tab
        theme_idx = self.combo_theme.findData(c.get("theme"))
        if theme_idx >= 0:
            self.combo_theme.setCurrentIndex(theme_idx)
            
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
        
        # Overlay Configuration
        c.set("overlay_enabled", self.chk_overlay_enabled.isChecked())
        c.set("overlay_unlocked", self.chk_overlay_unlocked.isChecked())
        c.set("overlay_opacity", self.slider_opacity.value() / 100.0)
        c.set("overlay_mode", self.combo_mode.currentData())
        c.set("key_highlight_color", self.combo_color.currentData())
        c.set("custom_layout_keys", self.txt_custom_keys.text())
        
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
        """Resets all options to default factory values."""
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

    # TAB UI CONSTRUCTORS
    def build_sound_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        # Enable Sound
        self.chk_sound_enabled = QCheckBox("Включить воспроизведение звуков")
        layout.addWidget(self.chk_sound_enabled)
        
        # Group file selector
        grp_file = QGroupBox("Файл звука")
        grp_file_layout = QVBoxLayout(grp_file)
        
        # Presets layout
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
        
        # Group sound parameters
        grp_params = QGroupBox("Параметры звука")
        grp_params_layout = QVBoxLayout(grp_params)
        
        # Volume slider
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
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        self.chk_overlay_enabled = QCheckBox("Отображать overlay клавиатуры")
        self.chk_overlay_unlocked = QCheckBox("Разблокировать перемещение overlay (перетаскивание)")
        layout.addWidget(self.chk_overlay_enabled)
        layout.addWidget(self.chk_overlay_unlocked)
        
        # Group overlay parameters
        grp_layout = QGroupBox("Параметры Overlay")
        grp_layout_layout = QVBoxLayout(grp_layout)
        
        # Opacity slider
        op_layout = QHBoxLayout()
        op_layout.addWidget(QLabel("Прозрачность:"))
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(0, 100)
        self.slider_opacity.valueChanged.connect(lambda val: self.lbl_opacity_val.setText(f"{val}%"))
        self.lbl_opacity_val = QLabel("85%")
        self.lbl_opacity_val.setFixedWidth(40)
        op_layout.addWidget(self.slider_opacity)
        op_layout.addWidget(self.lbl_opacity_val)
        grp_layout_layout.addLayout(op_layout)
        
        # Mode selector
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
        grp_layout_layout.addLayout(mode_layout)
        
        # Custom layout keys input
        self.custom_keys_layout = QHBoxLayout()
        self.lbl_custom_keys = QLabel("Клавиши раскладки (через запятую):")
        self.txt_custom_keys = QLineEdit()
        self.txt_custom_keys.setToolTip("Введите клавиши, например: q, w, e, r, d, f, space")
        self.custom_keys_layout.addWidget(self.lbl_custom_keys)
        self.custom_keys_layout.addWidget(self.txt_custom_keys)
        grp_layout_layout.addLayout(self.custom_keys_layout)
        
        self.combo_mode.currentIndexChanged.connect(self.toggle_custom_keys_visibility)
        
        # Key highlight color
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
        grp_layout_layout.addLayout(color_layout)
        
        layout.addWidget(grp_layout)
        
        # Reset position button
        self.btn_reset_pos = QPushButton("🔄 Сбросить позицию overlay")
        self.btn_reset_pos.clicked.connect(self.reset_overlay_position_triggered.emit)
        layout.addWidget(self.btn_reset_pos)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Overlay")

    def build_appearance_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(10)
        
        grp_theme = QGroupBox("Тема оформления приложения")
        grp_theme_layout = QVBoxLayout(grp_theme)
        
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Тема:"))
        self.combo_theme = QComboBox()
        self.combo_theme.addItem("Dark (Темная Fluent)", "dark")
        self.combo_theme.addItem("Light (Светлая Fluent)", "light")
        self.combo_theme.addItem("Glass (Полупрозрачное стекло)", "glass")
        self.combo_theme.addItem("Neon Blue (Киберпанк)", "neon")
        theme_layout.addWidget(self.combo_theme)
        grp_theme_layout.addLayout(theme_layout)
        
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
        
        # Reset all configs button
        self.btn_reset_all = QPushButton("⚠️ Сбросить настройки по умолчанию")
        self.btn_reset_all.clicked.connect(self.reset_settings)
        layout.addWidget(self.btn_reset_all)
        
        # Privacy Notice Banner
        lbl_privacy_title = QLabel("Безопасность и конфиденциальность:")
        lbl_privacy_title.setStyleSheet("font-weight: bold; margin-top: 10px; color: #888888;")
        layout.addWidget(lbl_privacy_title)
        
        lbl_privacy = QLabel(
            "Приложение использует глобальный keyboard hook исключительно для "
            "синхронизации подсветки клавиш overlay-панели и проигрывания кликов. "
            "Введенный текст нигде не сохраняется, не логируется и не передается по сети."
        )
        lbl_privacy.setWordWrap(True)
        lbl_privacy.setStyleSheet("font-size: 11px; color: #888888; font-style: italic; line-height: 14px;")
        layout.addWidget(lbl_privacy)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Система")

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
        """Plays the currently selected file path in settings (or default if blank)."""
        file_path = self.txt_sound_path.text()
        volume = self.slider_volume.value()
        self.sound_player.test_play(file_path, volume)
        
    def reject(self):
        """Override to just hide the settings instead of closing application context."""
        self.hide()
