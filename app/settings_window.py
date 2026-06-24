# app/settings_window.py
import os
import json
import re
from PySide6.QtWidgets import ( QGraphicsOpacityEffect,
    QDialog, QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget,
    QCheckBox, QLabel, QSlider, QPushButton, QComboBox,
    QFileDialog, QGroupBox, QLineEdit, QMessageBox, QColorDialog,
    QScrollArea, QFrame, QInputDialog, QListWidget, QListWidgetItem,
    QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Signal, QSize
from PySide6.QtGui import QColor, QFont, QIcon, QPixmap, QPainter

from app.themes import get_theme_qss, load_custom_themes, CUSTOM_THEMES
from app.utils import get_app_icon
from app.icons import get_icon
from app.autostart import set_autostart, is_autostart_enabled
from app.update_manager import UpdateCheckerWorker, CURRENT_VERSION
from app.profiles import ProfileManager


# ---------------------------------------------------------------------------
# Helper widgets
# ---------------------------------------------------------------------------

class ColorSelectorButton(QPushButton):
    """Button that opens a color picker and shows the selected color."""
    def __init__(self, initial_color, parent=None):
        super().__init__(parent)
        self.color = QColor(initial_color)
        self.setFixedWidth(80)
        self.update_style()
        self.clicked.connect(self.choose_color)

    def update_style(self):
        self.setStyleSheet(
            f"background-color: {self.color.name()};"
            f"border: 2px solid #555555; border-radius: 4px; min-height: 20px;"
        )

    def choose_color(self):
        color = QColorDialog.getColor(self.color, self, "Выберите цвет")
        if color.isValid():
            self.color = color
            self.update_style()


class SidebarButton(QPushButton):
    """Navigation button for the sidebar."""
    def __init__(self, icon_name, text, parent=None):
        super().__init__(parent)
        self.setText(f" {text}")
        self.setIcon(get_icon(icon_name, color="#AAAAAA", size=24))
        self.setIconSize(QSize(20, 20))
        self.setCheckable(True)
        self.setFixedHeight(44)
        self.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding-left: 12px;
                font-size: 13px;
                border: none;
                border-radius: 8px;
                background: transparent;
                color: #AAAAAA;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.06);
                color: #FFFFFF;
            }
            QPushButton:checked {
                background: rgba(0,120,212,0.25);
                color: #FFFFFF;
                font-weight: bold;
            }
        """)


class SectionLabel(QLabel):
    """Bold section header label inside a page."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #FFFFFF;"
            "margin-bottom: 4px; margin-top: 10px;"
        )


class DescLabel(QLabel):
    """Small grey description label."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.setStyleSheet("font-size: 11px; color: #888888; margin-bottom: 4px;")


class CardFrame(QFrame):
    """Rounded card container."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.04);
                border: 1px solid rgba(255,255,255,0.08);
                border-radius: 10px;
                padding: 4px;
            }
        """)


def slider_row(label_text, min_val, max_val, unit="", parent=None):
    """Creates a horizontal slider row, returns (layout, slider, value_label)."""
    row = QHBoxLayout()
    lbl = QLabel(label_text)
    lbl.setMinimumWidth(160)
    slider = QSlider(Qt.Horizontal)
    slider.setRange(min_val, max_val)
    val_lbl = QLabel(f"{min_val}{unit}")
    val_lbl.setFixedWidth(50)
    val_lbl.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
    slider.valueChanged.connect(lambda v: val_lbl.setText(f"{v}{unit}"))
    row.addWidget(lbl)
    row.addWidget(slider)
    row.addWidget(val_lbl)
    return row, slider, val_lbl


# ---------------------------------------------------------------------------
# Theme Creator Dialog
# ---------------------------------------------------------------------------

class ThemeCreatorDialog(QDialog):
    def __init__(self, app_data_dir, theme_qss, parent=None):
        super().__init__(parent)
        self.app_data_dir = app_data_dir
        self.created_theme_id = ""
        self.setWindowTitle("Конструктор тем")
        self.setWindowIcon(get_app_icon())
        self.resize(420, 540)
        self.setStyleSheet(theme_qss)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Название темы:"))
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("Например: Space Blue")
        name_row.addWidget(self.txt_name)
        layout.addLayout(name_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent;")
        sc = QWidget()
        scl = QVBoxLayout(sc)
        scl.setSpacing(10)
        scl.setContentsMargins(0, 0, 5, 0)

        grp_s = QGroupBox("Цвета окон настроек")
        gl_s = QVBoxLayout(grp_s)
        self.btn_win_bg = self._clr(gl_s, "Фон окон:", "#1F1F1F")
        self.btn_win_text = self._clr(gl_s, "Цвет текста:", "#FFFFFF")
        self.btn_win_accent = self._clr(gl_s, "Акцентный цвет:", "#0078D4")
        self.btn_win_card = self._clr(gl_s, "Фон карточек:", "#2D2D2D")
        self.btn_win_border = self._clr(gl_s, "Цвет рамок:", "#3D3D3D")
        scl.addWidget(grp_s)

        grp_o = QGroupBox("Цвета оверлея клавиш")
        gl_o = QVBoxLayout(grp_o)
        self.btn_key_idle_bg = self._clr(gl_o, "Фон клавиш (простой):", "#2D2D2D")
        self.btn_key_idle_border = self._clr(gl_o, "Рамка клавиш (простой):", "#3E3E3E")
        self.btn_key_idle_text = self._clr(gl_o, "Текст клавиш (простой):", "#FFFFFF")
        self.btn_key_active_bg = self._clr(gl_o, "Фон клавиш (нажатие):", "#0078D4")
        self.btn_key_active_border = self._clr(gl_o, "Рамка клавиш (нажатие):", "#FFFFFF")
        self.btn_key_active_text = self._clr(gl_o, "Текст клавиш (нажатие):", "#FFFFFF")

        r_row = QHBoxLayout()
        r_row.addWidget(QLabel("Скругление углов:"))
        self.slider_radius = QSlider(Qt.Horizontal)
        self.slider_radius.setRange(0, 15)
        self.slider_radius.setValue(5)
        self.lbl_r = QLabel("5px")
        self.lbl_r.setFixedWidth(40)
        self.slider_radius.valueChanged.connect(lambda v: self.lbl_r.setText(f"{v}px"))
        r_row.addWidget(self.slider_radius)
        r_row.addWidget(self.lbl_r)
        gl_o.addLayout(r_row)
        scl.addWidget(grp_o)

        scroll.setWidget(sc)
        layout.addWidget(scroll)

        btns = QHBoxLayout()
        btns.addStretch()
        btns.addWidget(QPushButton("Отмена", clicked=self.reject))
        save_btn = QPushButton("💾 Сохранить тему", clicked=self.save_theme)
        save_btn.setDefault(True)
        btns.addWidget(save_btn)
        layout.addLayout(btns)

    def _clr(self, layout, label, init):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        btn = ColorSelectorButton(init, self)
        row.addWidget(btn)
        layout.addLayout(row)
        return btn

    def save_theme(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название темы.")
            return
        theme_id = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
        theme_data = {
            "theme_display_name": name,
            "settings_window": {
                "background": self.btn_win_bg.color.name(),
                "text": self.btn_win_text.color.name(),
                "accent": self.btn_win_accent.color.name(),
                "card_bg": self.btn_win_card.color.name(),
                "border": self.btn_win_border.color.name(),
            },
            "overlay": {
                "key_idle_bg": f"rgba({self.btn_key_idle_bg.color.red()},{self.btn_key_idle_bg.color.green()},{self.btn_key_idle_bg.color.blue()},{self.btn_key_idle_bg.color.alpha()})",
                "key_idle_border": f"rgba({self.btn_key_idle_border.color.red()},{self.btn_key_idle_border.color.green()},{self.btn_key_idle_border.color.blue()},{self.btn_key_idle_border.color.alpha()})",
                "key_idle_text": self.btn_key_idle_text.color.name(),
                "key_active_bg": self.btn_key_active_bg.color.name(),
                "key_active_border": self.btn_key_active_border.color.name(),
                "key_active_text": self.btn_key_active_text.color.name(),
                "key_radius": self.slider_radius.value(),
                "container_bg": f"rgba({self.btn_win_bg.color.red()},{self.btn_win_bg.color.green()},{self.btn_win_bg.color.blue()},120)",
                "container_border": self.btn_win_accent.color.name(),
            },
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
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить тему:\n{e}")


# ---------------------------------------------------------------------------
# Main Settings Window — Sidebar Layout
# ---------------------------------------------------------------------------

class SettingsWindow(QDialog):
    settings_changed = Signal()
    reset_overlay_position_triggered = Signal()

    # Page indices
    PAGE_SOUND = 0
    PAGE_OVERLAY = 1
    PAGE_APPEARANCE = 2
    PAGE_PROFILES = 3
    PAGE_SYSTEM = 4

    def __init__(self, config, sound_player):
        super().__init__()
        self.config = config
        self.sound_player = sound_player
        self.custom_themes_list = load_custom_themes(self.config.app_data_dir)
        self.profile_mgr = ProfileManager(self.config.app_data_dir)

        self.setWindowTitle("KeySound Overlay — Настройки")
        self.setWindowIcon(get_app_icon())
        self.resize(720, 580)
        self.setMinimumSize(640, 500)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowContextHelpButtonHint
            | Qt.WindowCloseButtonHint
        )

        # Root layout: sidebar | content
        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────────────────────
        sidebar = QWidget()
        sidebar.setFixedWidth(195)
        sidebar.setObjectName("Sidebar")
        sidebar.setStyleSheet("""
            QWidget#Sidebar {
                background-color: #161616;
                border-right: 1px solid rgba(255,255,255,0.08);
            }
        """)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(10, 20, 10, 16)
        sb_layout.setSpacing(4)

        # App logo area
        logo_lbl = QLabel("🎹  KeySound")
        logo_lbl.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #0078D4;"
            "padding: 4px 8px 16px 8px;"
        )
        sb_layout.addWidget(logo_lbl)

        nav_items = [
            ("sound", "Звук"),
            ("keyboard", "Оверлей"),
            ("palette", "Внешний вид"),
            ("profile", "Профили"),
            ("settings", "Система"),
        ]
        self.nav_buttons = []
        for emoji, text in nav_items:
            btn = SidebarButton(emoji, text)
            btn.clicked.connect(self._make_nav_handler(len(self.nav_buttons)))
            sb_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sb_layout.addStretch()

        ver_lbl = QLabel(f"v{CURRENT_VERSION}")
        ver_lbl.setAlignment(Qt.AlignCenter)
        ver_lbl.setStyleSheet("color: #555555; font-size: 11px;")
        sb_layout.addWidget(ver_lbl)

        root.addWidget(sidebar)

        # ── Content area ─────────────────────────────────────────────────────
        content_wrap = QVBoxLayout()
        content_wrap.setContentsMargins(0, 0, 0, 0)
        content_wrap.setSpacing(0)

        self.stack = QStackedWidget()
        self.stack.addWidget(self._build_sound_page())
        self.stack.addWidget(self._build_overlay_page())
        self.stack.addWidget(self._build_appearance_page())
        self.stack.addWidget(self._build_profiles_page())
        self.stack.addWidget(self._build_system_page())

        content_wrap.addWidget(self.stack)

        # Bottom action buttons
        bottom_bar = QWidget()
        bottom_bar.setObjectName("BottomBar")
        bottom_bar.setStyleSheet("""
            QWidget#BottomBar {
                background-color: #1A1A1A;
                border-top: 1px solid rgba(255,255,255,0.08);
            }
        """)
        bb_layout = QHBoxLayout(bottom_bar)
        bb_layout.setContentsMargins(16, 10, 16, 10)
        bb_layout.setSpacing(8)
        bb_layout.addStretch()

        self.btn_apply = QPushButton("Применить")
        self.btn_apply.clicked.connect(self.apply_settings)
        self.btn_save = QPushButton("Сохранить и закрыть")
        self.btn_save.setIcon(get_icon("check", color="#FFFFFF"))
        self.btn_save.setDefault(True)
        self.btn_save.clicked.connect(self.save_and_close)
        self.btn_save.setStyleSheet(
            "background-color: #0078D4; color: white; font-weight: bold;"
            "padding: 7px 18px; border-radius: 6px;"
        )

        bb_layout.addWidget(self.btn_apply)
        bb_layout.addWidget(self.btn_save)

        content_wrap.addWidget(bottom_bar)
        root.addLayout(content_wrap)

        # Select first page
        self._switch_page(0)

        # Load values and apply theme
        self.load_values()
        self.apply_theme_styling()

    # ── Navigation ───────────────────────────────────────────────────────────

    def _make_nav_handler(self, idx):
        return lambda: self._switch_page(idx)

    def _switch_page(self, idx):
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
        self.anim.start()

    def apply_theme_styling(self):
        theme_name = self.config.get("theme")
        self.setStyleSheet(get_theme_qss(theme_name))
        # Re-apply sidebar/bottom bar overrides (theme resets them)
        for child in self.findChildren(QWidget, "Sidebar"):
            child.setStyleSheet("""
                QWidget#Sidebar {
                    background-color: #161616;
                    border-right: 1px solid rgba(255,255,255,0.08);
                }
            """)

    # ── Pages ─────────────────────────────────────────────────────────────────

    def _scrollable_page(self):
        """Returns (page_widget, inner_layout) for a scrollable content page."""
        page = QWidget()
        page.setObjectName("ContentPage")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        inner = QWidget()
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(24, 20, 24, 20)
        inner_layout.setSpacing(14)

        scroll.setWidget(inner)
        page_layout.addWidget(scroll)
        return page, inner_layout

    def _build_sound_page(self):
        page, lay = self._scrollable_page()

        lay.addWidget(SectionLabel("Звук клавиш"))

        # Enable toggle
        self.chk_sound_enabled = QCheckBox("Включить воспроизведение звуков")
        lay.addWidget(self.chk_sound_enabled)

        # Preset selection card
        card1 = CardFrame()
        c1l = QVBoxLayout(card1)
        c1l.setContentsMargins(12, 12, 12, 12)
        c1l.setSpacing(8)
        c1l.addWidget(QLabel("Предустановленный свич:"))

        self.combo_presets = QComboBox()
        self.combo_presets.addItem("По умолчанию (встроенный клик)", "")

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
        self.combo_presets.addItem("Другой звуковой файл...", "custom")
        
        # Disable category headers
        model = self.combo_presets.model()
        for i in range(self.combo_presets.count()):
            if self.combo_presets.itemData(i) is None:
                item = model.item(i)
                if item:
                    item.setEnabled(False)
        self.combo_presets.currentIndexChanged.connect(self.preset_changed)
        c1l.addWidget(self.combo_presets)

        file_row = QHBoxLayout()
        self.txt_sound_path = QLineEdit()
        self.txt_sound_path.setPlaceholderText("По умолчанию (встроенный клик)")
        self.btn_browse = QPushButton("Обзор…")
        self.btn_browse.clicked.connect(self.browse_sound_file)
        self.btn_browse.setFixedWidth(80)
        file_row.addWidget(self.txt_sound_path)
        file_row.addWidget(self.btn_browse)
        c1l.addLayout(file_row)

        self.btn_test = QPushButton("Тест звука")
        self.btn_test.setIcon(get_icon("play", color="#FFFFFF"))
        self.btn_test.clicked.connect(self.test_sound_file)
        c1l.addWidget(self.btn_test)
        lay.addWidget(card1)

        # Volume/params card
        card2 = CardFrame()
        c2l = QVBoxLayout(card2)
        c2l.setContentsMargins(12, 12, 12, 12)
        c2l.setSpacing(8)
        c2l.addWidget(QLabel("Параметры:"))

        vol_row, self.slider_volume, self.lbl_volume_val = slider_row("Громкость:", 0, 100, "%")
        c2l.addLayout(vol_row)

        self.chk_pitch_rand = QCheckBox("Живой звук (случайный pitch и громкость)")
        self.chk_repeat_hold = QCheckBox("Повторять звук при удержании клавиши")
        c2l.addWidget(self.chk_pitch_rand)
        c2l.addWidget(self.chk_repeat_hold)
        lay.addWidget(card2)

        lay.addStretch()
        return page

    def _build_overlay_page(self):
        page, lay = self._scrollable_page()
        lay.addWidget(SectionLabel("Оверлей клавиатуры"))

        card_kb = CardFrame()
        kb_l = QVBoxLayout(card_kb)
        kb_l.setContentsMargins(12, 12, 12, 12)
        kb_l.setSpacing(8)

        self.chk_overlay_enabled = QCheckBox("Показывать оверлей клавиатуры")
        self.chk_overlay_unlocked = QCheckBox("Разблокировать перетаскивание")
        kb_l.addWidget(self.chk_overlay_enabled)
        kb_l.addWidget(self.chk_overlay_unlocked)

        op_row, self.slider_opacity, self.lbl_opacity_val = slider_row("Прозрачность:", 0, 100, "%")
        kb_l.addLayout(op_row)

        mode_row = QHBoxLayout()
        mode_row.addWidget(QLabel("Режим отображения:"))
        self.combo_mode = QComboBox()
        self.combo_mode.addItem("Полная клавиатура", "full")
        self.combo_mode.addItem("Игровой (WASD + Space + Modifiers)", "wasd")
        self.combo_mode.addItem("Кликер Osu! (Z + X + Space + Esc)", "osu")
        self.combo_mode.addItem("Dota 2 (Панель клавиш)", "dota")
        self.combo_mode.addItem("Своя раскладка (Кастомная)", "custom")
        self.combo_mode.addItem("Только нажатые клавиши (лог)", "pressed")
        self.combo_mode.currentIndexChanged.connect(self.toggle_custom_keys_visibility)
        mode_row.addWidget(self.combo_mode)
        kb_l.addLayout(mode_row)

        self.lbl_custom_keys = QLabel("Клавиши (через запятую):")
        self.txt_custom_keys = QLineEdit()
        self.txt_custom_keys.setToolTip("Например: q, w, e, r, d, f, space")
        kb_l.addWidget(self.lbl_custom_keys)
        kb_l.addWidget(self.txt_custom_keys)

        color_row = QHBoxLayout()
        color_row.addWidget(QLabel("Цвет подсветки:"))
        self.combo_color = QComboBox()
        self.combo_color.addItem("Windows Blue", "#0078D4")
        self.combo_color.addItem("Neon Cyan", "#00F0FF")
        self.combo_color.addItem("Cyber Pink", "#FF007F")
        self.combo_color.addItem("Acid Green", "#10B981")
        self.combo_color.addItem("Vivid Purple", "#B400FF")
        self.combo_color.addItem("Sunset Orange", "#FF5722")
        color_row.addWidget(self.combo_color)
        kb_l.addLayout(color_row)
        lay.addWidget(card_kb)

        # Animation & fullscreen
        lay.addWidget(SectionLabel("Эффекты"))
        card_fx = CardFrame()
        fx_l = QVBoxLayout(card_fx)
        fx_l.setContentsMargins(12, 12, 12, 12)
        fx_l.setSpacing(8)
        self.combo_anim = QComboBox()
        self.combo_anim.addItem("Рябь (Ripple)", "ripple")
        self.combo_anim.addItem("Затухание (Fade)", "fade")
        self.combo_anim.addItem("Прыжок (Bounce)", "bounce")
        self.combo_anim.addItem("Без анимации", "none")
        self.chk_show_fullscreen = QCheckBox("Показывать оверлей поверх полноэкранных приложений")
        fx_l.addWidget(QLabel("Анимация нажатия:"))
        fx_l.addWidget(self.combo_anim)
        fx_l.addWidget(self.chk_show_fullscreen)
        lay.addWidget(card_fx)

        # Mouse overlay
        lay.addWidget(SectionLabel("Оверлей мыши"))
        card_mouse = CardFrame()
        ml = QVBoxLayout(card_mouse)
        ml.setContentsMargins(12, 12, 12, 12)
        ml.setSpacing(8)

        self.chk_mouse_enabled = QCheckBox("Показывать оверлей мыши")
        self.chk_mouse_show_coords = QCheckBox("Показывать координаты мыши")
        self.chk_mouse_show_clicks = QCheckBox("Подсвечивать клики кнопок")
        self.chk_mouse_unlocked = QCheckBox("Разблокировать перемещение оверлея мыши")
        ml.addWidget(self.chk_mouse_enabled)
        ml.addWidget(self.chk_mouse_show_coords)
        ml.addWidget(self.chk_mouse_show_clicks)
        ml.addWidget(self.chk_mouse_unlocked)

        mop_row, self.slider_mouse_opacity, self.lbl_mouse_opacity_val = slider_row(
            "Прозрачность мыши:", 0, 100, "%"
        )
        ml.addLayout(mop_row)
        lay.addWidget(card_mouse)

        # Reset positions
        self.btn_reset_pos = QPushButton("Сбросить позиции оверлеев")
        self.btn_reset_pos.setIcon(get_icon("resize", color="#FFFFFF"))
        self.btn_reset_pos.clicked.connect(self.reset_overlay_position_triggered.emit)
        lay.addWidget(self.btn_reset_pos)

        lay.addStretch()
        return page

    def _build_appearance_page(self):
        page, lay = self._scrollable_page()
        lay.addWidget(SectionLabel("Внешний вид"))

        card_th = CardFrame()
        th_l = QVBoxLayout(card_th)
        th_l.setContentsMargins(12, 12, 12, 12)
        th_l.setSpacing(10)
        th_l.addWidget(QLabel("Активная тема:"))

        self.combo_theme = QComboBox()
        th_l.addWidget(self.combo_theme)

        th_l.addWidget(DescLabel(
            "Тема влияет на цвета окна настроек и оверлея. "
            "Создайте свою тему через кнопку ниже."
        ))

        self.btn_create_theme = QPushButton("Создать кастомную тему…")
        self.btn_create_theme.setIcon(get_icon("palette", color="#FFFFFF"))
        self.btn_create_theme.clicked.connect(self.open_theme_creator)
        th_l.addWidget(self.btn_create_theme)
        lay.addWidget(card_th)

        lay.addStretch()
        return page

    def _build_profiles_page(self):
        page, lay = self._scrollable_page()
        lay.addWidget(SectionLabel("Профили настроек"))
        lay.addWidget(DescLabel(
            "Профили позволяют сохранять и переключаться между разными наборами настроек — "
            "например, для стриминга и для игры."
        ))

        card_p = CardFrame()
        pl = QVBoxLayout(card_p)
        pl.setContentsMargins(12, 12, 12, 12)
        pl.setSpacing(10)

        pl.addWidget(QLabel("Список профилей:"))
        self.lst_profiles = QListWidget()
        self.lst_profiles.setFixedHeight(160)
        self.lst_profiles.setStyleSheet(
            "QListWidget { border-radius: 6px; border: 1px solid rgba(255,255,255,0.1); }"
            "QListWidget::item:selected { background: rgba(0,120,212,0.35); border-radius: 4px; }"
        )
        pl.addWidget(self.lst_profiles)

        btns_row = QHBoxLayout()
        self.btn_profile_save = QPushButton("Сохранить текущий")
        self.btn_profile_save.setIcon(get_icon("save", color="#FFFFFF"))
        self.btn_profile_load = QPushButton("Загрузить")
        self.btn_profile_load.setIcon(get_icon("load", color="#FFFFFF"))
        self.btn_profile_delete = QPushButton("Удалить")
        self.btn_profile_delete.setIcon(get_icon("trash", color="#FFFFFF"))
        self.btn_profile_save.clicked.connect(self.save_profile)
        self.btn_profile_load.clicked.connect(self.load_profile)
        self.btn_profile_delete.clicked.connect(self.delete_profile)
        btns_row.addWidget(self.btn_profile_save)
        btns_row.addWidget(self.btn_profile_load)
        btns_row.addWidget(self.btn_profile_delete)
        pl.addLayout(btns_row)
        lay.addWidget(card_p)

        lay.addStretch()
        return page

    def _build_system_page(self):
        page, lay = self._scrollable_page()
        lay.addWidget(SectionLabel("Система"))

        card_sys = CardFrame()
        sl = QVBoxLayout(card_sys)
        sl.setContentsMargins(12, 12, 12, 12)
        sl.setSpacing(8)
        self.chk_autostart = QCheckBox("Запускать вместе с Windows")
        self.chk_minimize_tray = QCheckBox("Сворачивать в трей при закрытии")
        self.chk_start_minimized = QCheckBox("Запускать скрытым (только в трее)")
        sl.addWidget(self.chk_autostart)
        sl.addWidget(self.chk_minimize_tray)
        sl.addWidget(self.chk_start_minimized)
        lay.addWidget(card_sys)

        lay.addWidget(SectionLabel("Обновления"))
        card_upd = CardFrame()
        ul = QVBoxLayout(card_upd)
        ul.setContentsMargins(12, 12, 12, 12)
        ul.setSpacing(8)
        self.lbl_app_version = QLabel(f"Текущая версия: {CURRENT_VERSION}")
        self.chk_check_startup = QCheckBox("Проверять обновления при запуске")
        ul.addWidget(self.lbl_app_version)
        ul.addWidget(self.chk_check_startup)

        upd_btns = QHBoxLayout()
        self.btn_check_updates = QPushButton("Проверить обновления")
        self.btn_check_updates.setIcon(get_icon("search", color="#FFFFFF"))
        self.btn_check_updates.clicked.connect(self.check_for_updates_clicked)
        self.btn_install_update = QPushButton("Установить обновление")
        self.btn_install_update.setIcon(get_icon("update", color="#FFFFFF"))
        self.btn_install_update.setStyleSheet(
            "background-color: #10B981; color: white; font-weight: bold;"
        )
        self.btn_install_update.setVisible(False)
        self.btn_install_update.clicked.connect(self.run_update_dialog)
        upd_btns.addWidget(self.btn_check_updates)
        upd_btns.addWidget(self.btn_install_update)
        ul.addLayout(upd_btns)
        lay.addWidget(card_upd)

        self.btn_reset_all = QPushButton("Сбросить все настройки по умолчанию")
        self.btn_reset_all.setIcon(get_icon("warning", color="#FFFFFF"))
        self.btn_reset_all.clicked.connect(self.reset_settings)
        lay.addWidget(self.btn_reset_all)

        priv = DescLabel(
            "Приложение использует глобальный hook исключительно для отображения "
            "подсветки клавиатуры/мыши и воспроизведения звуков. Никакие данные "
            "не сохраняются и не отправляются в сеть."
        )
        lay.addWidget(priv)
        lay.addStretch()
        return page

    # ── Load / Apply / Save ───────────────────────────────────────────────────

    def load_values(self):
        c = self.config

        # Sound
        self.chk_sound_enabled.setChecked(c.get("sound_enabled"))
        self.txt_sound_path.setText(c.get("sound_file"))
        self.slider_volume.setValue(c.get("volume"))
        self.lbl_volume_val.setText(f"{c.get('volume')}%")
        self.chk_pitch_rand.setChecked(c.get("pitch_randomize"))
        self.chk_repeat_hold.setChecked(c.get("repeat_on_hold"))

        sound_file = c.get("sound_file")
        self.combo_presets.blockSignals(True)
        if not sound_file:
            self.combo_presets.setCurrentIndex(0)
        else:
            matched = False
            for idx in range(self.combo_presets.count()):
                p_data = self.combo_presets.itemData(idx)
                if p_data and p_data not in ("custom", None):
                    if sound_file.replace("\\", "/").lower().endswith(p_data.lower()):
                        self.combo_presets.setCurrentIndex(idx)
                        matched = True
                        break
            if not matched:
                self.combo_presets.setCurrentIndex(self.combo_presets.count() - 1)
        self.combo_presets.blockSignals(False)

        # Overlay
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

        anim_val = c.get("key_press_animation", "ripple")
        if anim_val is True: anim_val = "ripple"
        if anim_val is False: anim_val = "none"
        idx = self.combo_anim.findData(anim_val)
        if idx >= 0: self.combo_anim.setCurrentIndex(idx)
        self.chk_show_fullscreen.setChecked(c.get("show_in_fullscreen"))

        # Mouse
        self.chk_mouse_enabled.setChecked(c.get("mouse_overlay_enabled"))
        self.chk_mouse_show_coords.setChecked(c.get("mouse_overlay_show_coords"))
        self.chk_mouse_show_clicks.setChecked(c.get("mouse_overlay_show_clicks"))
        self.chk_mouse_unlocked.setChecked(c.get("mouse_overlay_unlocked"))
        m_op = c.get("mouse_overlay_opacity")
        self.slider_mouse_opacity.setValue(int(m_op * 100))
        self.lbl_mouse_opacity_val.setText(f"{int(m_op * 100)}%")

        # Appearance
        self.combo_theme.blockSignals(True)
        self.combo_theme.clear()
        self.combo_theme.addItem("Dark (Тёмная Fluent)", "dark")
        self.combo_theme.addItem("Light (Светлая Fluent)", "light")
        self.combo_theme.addItem("Glass (Полупрозрачное стекло)", "glass")
        self.combo_theme.addItem("Neon Blue (Киберпанк)", "neon")
        for display_name, theme_id in self.custom_themes_list:
            self.combo_theme.addItem(f"Кастомная: {display_name}", theme_id)
        theme_idx = self.combo_theme.findData(c.get("theme"))
        self.combo_theme.setCurrentIndex(theme_idx if theme_idx >= 0 else 0)
        self.combo_theme.blockSignals(False)

        # Profiles list
        self._refresh_profiles_list()

        # System
        self.chk_autostart.setChecked(is_autostart_enabled())
        self.chk_minimize_tray.setChecked(c.get("minimize_to_tray"))
        self.chk_start_minimized.setChecked(c.get("start_minimized"))
        self.chk_check_startup.setChecked(c.get("check_updates_on_startup"))

    def apply_settings(self):
        c = self.config

        # Sound
        c.set("sound_enabled", self.chk_sound_enabled.isChecked())
        c.set("sound_file", self.txt_sound_path.text())
        c.set("volume", self.slider_volume.value())
        c.set("pitch_randomize", self.chk_pitch_rand.isChecked())
        c.set("repeat_on_hold", self.chk_repeat_hold.isChecked())

        # Keyboard Overlay
        c.set("overlay_enabled", self.chk_overlay_enabled.isChecked())
        c.set("overlay_unlocked", self.chk_overlay_unlocked.isChecked())
        c.set("overlay_opacity", self.slider_opacity.value() / 100.0)
        c.set("overlay_mode", self.combo_mode.currentData())
        c.set("key_highlight_color", self.combo_color.currentData())
        c.set("custom_layout_keys", self.txt_custom_keys.text())
        c.set("key_press_animation", self.combo_anim.currentData())
        c.set("show_in_fullscreen", self.chk_show_fullscreen.isChecked())

        # Mouse Overlay
        c.set("mouse_overlay_enabled", self.chk_mouse_enabled.isChecked())
        c.set("mouse_overlay_show_coords", self.chk_mouse_show_coords.isChecked())
        c.set("mouse_overlay_show_clicks", self.chk_mouse_show_clicks.isChecked())
        c.set("mouse_overlay_unlocked", self.chk_mouse_unlocked.isChecked())
        c.set("mouse_overlay_opacity", self.slider_mouse_opacity.value() / 100.0)

        # Appearance
        c.set("theme", self.combo_theme.currentData())

        # System
        c.set("minimize_to_tray", self.chk_minimize_tray.isChecked())
        c.set("start_minimized", self.chk_start_minimized.isChecked())
        c.set("check_updates_on_startup", self.chk_check_startup.isChecked())

        autostart_req = self.chk_autostart.isChecked()
        if autostart_req != is_autostart_enabled():
            set_autostart(autostart_req)

        c.save()
        self.sound_player.reload()
        self.apply_theme_styling()
        self.settings_changed.emit()

    def save_and_close(self):
        self.apply_settings()
        self.accept()

    def reset_settings(self):
        reply = QMessageBox.question(
            self, "Сброс настроек",
            "Сбросить все настройки на значения по умолчанию?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.config.reset()
            self.load_values()
            self.apply_settings()

    # ── Profile actions ───────────────────────────────────────────────────────

    def _refresh_profiles_list(self):
        self.lst_profiles.clear()
        for name in self.profile_mgr.list_profiles():
            display = self.profile_mgr.get_display_name(name)
            item = QListWidgetItem(f" {display}")
            item.setIcon(get_icon("profile", color="#AAAAAA"))
            item.setData(Qt.UserRole, name)
            self.lst_profiles.addItem(item)

    def save_profile(self):
        self.apply_settings()
        name, ok = QInputDialog.getText(self, "Сохранить профиль", "Название профиля:")
        if ok and name.strip():
            ok2 = self.profile_mgr.save_profile(name.strip(), dict(self.config.settings))
            if ok2:
                self._refresh_profiles_list()
                QMessageBox.information(self, "Профиль", f"Профиль «{name}» сохранён!")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить профиль.")

    def load_profile(self):
        item = self.lst_profiles.currentItem()
        if not item:
            QMessageBox.information(self, "Профили", "Выберите профиль из списка.")
            return
        name = item.data(Qt.UserRole)
        settings = self.profile_mgr.load_profile(name)
        if settings is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить профиль.")
            return
        for key, val in settings.items():
            if key in self.config.settings:
                self.config.settings[key] = val
        self.config.save()
        self.load_values()
        self.apply_settings()
        QMessageBox.information(self, "Профиль", f"Профиль «{self.profile_mgr.get_display_name(name)}» загружен!")

    def delete_profile(self):
        item = self.lst_profiles.currentItem()
        if not item:
            return
        name = item.data(Qt.UserRole)
        display = self.profile_mgr.get_display_name(name)
        reply = QMessageBox.question(
            self, "Удаление профиля",
            f"Удалить профиль «{display}»?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.profile_mgr.delete_profile(name)
            self._refresh_profiles_list()

    # ── Sound helpers ─────────────────────────────────────────────────────────

    def preset_changed(self, index):
        data = self.combo_presets.itemData(index)
        if data is None:
            # Separator — revert to previous valid item
            return
        if data == "custom":
            pass
        elif data == "":
            self.txt_sound_path.setText("")
        else:
            from app.utils import get_resource_path
            self.txt_sound_path.setText(get_resource_path(data))

    def browse_sound_file(self):
        file_filter = "Звуковые файлы (*.wav *.mp3 *.ogg);;All (*)"
        path, _ = QFileDialog.getOpenFileName(self, "Выберите файл звука", "", file_filter)
        if path:
            self.txt_sound_path.setText(path)
            custom_idx = self.combo_presets.findData("custom")
            if custom_idx >= 0:
                self.combo_presets.setCurrentIndex(custom_idx)

    def test_sound_file(self):
        self.sound_player.test_play(self.txt_sound_path.text(), self.slider_volume.value())

    def toggle_custom_keys_visibility(self):
        is_custom = self.combo_mode.currentData() == "custom"
        self.lbl_custom_keys.setVisible(is_custom)
        self.txt_custom_keys.setVisible(is_custom)

    # ── Update helpers ────────────────────────────────────────────────────────

    def check_for_updates_clicked(self):
        self.btn_check_updates.setEnabled(False)
        self.btn_check_updates.setText("Проверка…")
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
            self.lbl_app_version.setText(
                f"Версия: {CURRENT_VERSION}  ➜  🆕 Доступна {latest_version}!"
            )
            self.run_update_dialog()
        else:
            self.btn_install_update.setVisible(False)
            self.lbl_app_version.setText(f"Версия: {CURRENT_VERSION}  ✅ Актуальная")
            QMessageBox.information(self, "Обновление", "У вас установлена последняя версия!")

    def on_settings_update_failed(self, error_msg):
        self.btn_check_updates.setEnabled(True)
        self.btn_check_updates.setText("Проверить обновления")
        QMessageBox.warning(self, "Ошибка", f"Не удалось проверить обновления:\n{error_msg}")

    def run_update_dialog(self):
        if hasattr(self, "latest_version") and self.download_url:
            from app.update_dialog import UpdateDialog
            dlg = UpdateDialog(self.config, self)
            dlg.set_update_info(self.latest_version, self.changelog, self.download_url)
            dlg.exec()

    def open_theme_creator(self):
        dlg = ThemeCreatorDialog(
            self.config.app_data_dir, get_theme_qss(self.config.get("theme")), self
        )
        if dlg.exec():
            self.custom_themes_list = load_custom_themes(self.config.app_data_dir)
            self.load_values()
            created_id = dlg.created_theme_id
            self.config.set("theme", created_id)
            self.apply_theme_styling()
            self.settings_changed.emit()

    def reject(self):
        self.hide()
