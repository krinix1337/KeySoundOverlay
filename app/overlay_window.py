# app/overlay_window.py
import ctypes
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation
from PySide6.QtGui import QColor, QPainter, QFont, QPen, QBrush
from app.themes import get_overlay_key_qss

# Windows API Constants
GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED = 0x00080000

def set_click_through(hwnd, enabled):
    """Enables or disables click-through on a window handle via Windows API."""
    if not hwnd:
        return False
    try:
        user32 = ctypes.windll.user32
        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        if enabled:
            style |= (WS_EX_TRANSPARENT | WS_EX_LAYERED)
        else:
            style &= ~WS_EX_TRANSPARENT
        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # Force frame update
        user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0x0027) # SWP_FRAMECHANGED | SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER
        return True
    except Exception as e:
        print(f"Error configuration WinAPI click-through: {e}")
        return False

KEY_MAP_LABELS = {
    "esc": "ESC", "space": "Space", "backspace": "⌫", "tab": "Tab", "caps_lock": "Caps",
    "enter": "Enter", "shift_l": "Shift", "shift_r": "Shift", "ctrl_l": "Ctrl", "ctrl_r": "Ctrl",
    "alt_l": "Alt", "alt_r": "Alt", "win": "Win", "up": "▲", "down": "▼", "left": "◀", "right": "▶"
}

class KeyCap(QLabel):
    """Custom styled keycap widget that responds to press and release states."""
    def __init__(self, key_id, display_text, parent=None):
        super().__init__(display_text, parent)
        self.key_id = key_id
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(False)
        self.is_pressed = False

    def update_style(self, theme_name, highlight_color, opacity=1.0):
        """Updates styling based on current state and theme."""
        style = get_overlay_key_qss(theme_name, highlight_color, self.is_pressed, opacity)
        self.setStyleSheet(style)

class OverlayWindow(QWidget):
    def __init__(self, config, sound_player):
        super().__init__()
        self.config = config
        self.sound_player = sound_player
        self.drag_position = QPoint()
        self.key_widgets = {} # Maps key name strings to KeyCap widgets
        self.pressed_key_items = [] # History track of labels for 'pressed' mode
        
        # Window attributes setup
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setMouseTracking(True)
        
        # Create container QFrame for drawing optional unlocked borders
        self.container = QFrame(self)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(4, 4, 4, 4)
        self.container.setObjectName("ContainerFrame")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)
        
        self.reload_ui()

    def get_layout_size(self):
        """Calculates size of window based on selected layout mode."""
        mode = self.config.get("overlay_mode")
        if mode == "full":
            return (610, 215)
        elif mode == "wasd":
            return (270, 140)
        elif mode == "osu":
            return (150, 140)
        elif mode == "dota":
            return (340, 170)
        elif mode == "pressed":
            return (360, 50)
        elif mode == "custom":
            custom_keys_str = self.config.get("custom_layout_keys")
            keys = [k.strip().lower() for k in custom_keys_str.split(",") if k.strip()]
            num_keys = len(keys) if keys else 4
            row_size = 8
            num_rows = (num_keys + row_size - 1) // row_size
            if num_rows == 0:
                num_rows = 1
            
            max_row_width = 0
            for i in range(0, num_keys, row_size):
                row_keys = keys[i:i+row_size]
                row_w = 0
                for k in row_keys:
                    if k == "space":
                        row_w += 120
                    elif k in ("shift_l", "shift_r", "enter", "backspace"):
                        row_w += 65
                    elif k in ("ctrl_l", "ctrl_r", "alt_l", "alt_r", "tab", "caps_lock"):
                        row_w += 50
                    else:
                        row_w += 40
                    row_w += 8
                if row_w > 0:
                    row_w -= 8
                if row_w > max_row_width:
                    max_row_width = row_w
            
            w = max(150, max_row_width + 16)
            h = num_rows * 40 + (num_rows - 1) * 8 + 16
            return (w, h)
        return (800, 260)

    def reload_ui(self):
        """Rebuilds the overlay layout depending on current settings."""
        # Clean current container layouts and widgets
        self.key_widgets.clear()
        
        if self.container.layout() is not None:
            def recursive_delete(layout):
                while layout.count():
                    item = layout.takeAt(0)
                    w = item.widget()
                    if w:
                        w.setParent(None)
                        w.deleteLater()
                    else:
                        l = item.layout()
                        if l:
                            recursive_delete(l)
                            l.deleteLater()
            recursive_delete(self.container_layout)
        else:
            self.container_layout = QVBoxLayout(self.container)
            
        self.container_layout.setContentsMargins(4, 4, 4, 4)
                
        # Keep window opacity at 1.0 so text and highlight colors are fully bright and visible.
        # Translucency of background is managed by drawing RGBA backgrounds.
        self.setWindowOpacity(1.0)
        
        # Load window geometry and resize window according to layout
        x = self.config.get("overlay_x")
        y = self.config.get("overlay_y")
        w, h = self.get_layout_size()
        self.setGeometry(x, y, w, h)
        self.setFixedSize(w, h)
        
        # Render specific mode
        mode = self.config.get("overlay_mode")
        if mode == "full":
            self.build_full_layout()
        elif mode == "wasd":
            self.build_wasd_layout()
        elif mode == "osu":
            self.build_osu_layout()
        elif mode == "dota":
            self.build_dota_layout()
        elif mode == "custom":
            self.build_custom_layout()
        elif mode == "pressed":
            self.build_pressed_layout()
            
        self.update_appearance()
        self.update_click_through_state()

    def update_click_through_state(self):
        """Toggles window interaction click-through based on settings."""
        unlocked = self.config.get("overlay_unlocked")
        hwnd = int(self.winId())
        set_click_through(hwnd, not unlocked)
        
        # Redraw container borders and background base plate to hint drag availability
        accent = self.config.get("key_highlight_color")
        theme = self.config.get("theme").lower()
        opacity = self.config.get("overlay_opacity")
        alpha = int(opacity * 180) # Semi-transparent base plate background when locked
        
        if unlocked:
            self.container.setStyleSheet(f"""
                QFrame#ContainerFrame {{
                    border: 2px dashed {accent};
                    background-color: rgba(20, 20, 20, 160);
                    border-radius: 8px;
                }}
            """)
        else:
            if theme == "light":
                self.container.setStyleSheet(f"""
                    QFrame#ContainerFrame {{
                        border: none;
                        background-color: rgba(240, 240, 240, {alpha});
                        border-radius: 8px;
                    }}
                """)
            elif theme == "glass":
                border_alpha = int(opacity * 30)
                self.container.setStyleSheet(f"""
                    QFrame#ContainerFrame {{
                        border: 1px solid rgba(255, 255, 255, {border_alpha});
                        background-color: rgba(25, 25, 25, {int(opacity * 110)});
                        border-radius: 8px;
                    }}
                """)
            elif theme == "neon":
                border_alpha = int(opacity * 60)
                self.container.setStyleSheet(f"""
                    QFrame#ContainerFrame {{
                        border: 1px solid rgba(0, 240, 255, {border_alpha});
                        background-color: rgba(5, 8, 17, {alpha});
                        border-radius: 8px;
                    }}
                """)
            else: # dark (default)
                self.container.setStyleSheet(f"""
                    QFrame#ContainerFrame {{
                        border: none;
                        background-color: rgba(20, 20, 20, {alpha});
                        border-radius: 8px;
                    }}
                """)

    def update_appearance(self):
        """Updates styling parameters on all keycap subcomponents."""
        theme = self.config.get("theme")
        accent = self.config.get("key_highlight_color")
        opacity = self.config.get("overlay_opacity")
        for key_name, widget in self.key_widgets.items():
            if hasattr(widget, 'update_style'):
                widget.update_style(theme, accent, opacity)

    def set_key_state(self, key_name, is_pressed):
        """Triggered from keyboard hook thread signals."""
        # Play Sound on Key Down
        if is_pressed and self.config.get("sound_enabled"):
            self.sound_player.play_click()
            
        # Update keycaps for Full and WASD layout
        if key_name in self.key_widgets:
            widget = self.key_widgets[key_name]
            if hasattr(widget, 'update_style'):
                widget.is_pressed = is_pressed
                theme = self.config.get("theme")
                accent = self.config.get("key_highlight_color")
                opacity = self.config.get("overlay_opacity")
                widget.update_style(theme, accent, opacity)
            
        # Update dynamically for History/Pressed mode
        if is_pressed and self.config.get("overlay_mode") == "pressed":
            self.add_pressed_key_history(key_name)

    # LAYOUT BUILDERS
    def build_full_layout(self):
        # Rows definition of standard full ANSI keyboard
        rows = [
            # Row 1 (Esc + Fs)
            [("esc", "ESC", 40), (None, "", 20), ("f1", "F1", 35), ("f2", "F2", 35), ("f3", "F3", 35), ("f4", "F4", 35), 
             (None, "", 15), ("f5", "F5", 35), ("f6", "F6", 35), ("f7", "F7", 35), ("f8", "F8", 35),
             (None, "", 15), ("f9", "F9", 35), ("f10", "F10", 35), ("f11", "F11", 35), ("f12", "F12", 35)],
            # Row 2 (Digits)
            [("`", "`", 35), ("1", "1", 35), ("2", "2", 35), ("3", "3", 35), ("4", "4", 35), ("5", "5", 35), 
             ("6", "6", 35), ("7", "7", 35), ("8", "8", 35), ("9", "9", 35), ("0", "0", 35), ("-", "-", 35), 
             ("=", "=", 35), ("backspace", "⌫", 70)],
            # Row 3 (Tab + QWE)
            [("tab", "Tab", 50), ("q", "Q", 35), ("w", "W", 35), ("e", "E", 35), ("r", "R", 35), ("t", "T", 35), 
             ("y", "Y", 35), ("u", "U", 35), ("i", "I", 35), ("o", "O", 35), ("p", "P", 35), 
             ("[", "[", 35), ("]", "]", 35), ("\\", "\\", 45)],
            # Row 4 (Caps + ASD)
            [("caps_lock", "Caps", 60), ("a", "A", 35), ("s", "S", 35), ("d", "D", 35), ("f", "F", 35), ("g", "G", 35), 
             ("h", "H", 35), ("j", "J", 35), ("k", "K", 35), ("l", "L", 35), (";", ";", 35), ("'", "'", 35), 
             ("enter", "Enter", 75)],
            # Row 5 (Shift + ZXC + Arrows helper)
            [("shift_l", "Shift", 80), ("z", "Z", 35), ("x", "X", 35), ("c", "C", 35), ("v", "V", 35), ("b", "B", 35), 
             ("n", "N", 35), ("m", "M", 35), (",", ",", 35), (".", ".", 35), ("/", "/", 35), 
             ("shift_r", "Shift", 90), (None, "", 10), ("up", "▲", 35)],
            # Row 6 (Controls + Space + Arrows)
            [("ctrl_l", "Ctrl", 55), ("win", "Win", 45), ("alt_l", "Alt", 45), ("space", "Space", 240), 
             ("alt_r", "Alt", 45), ("ctrl_r", "Ctrl", 55), (None, "", 5), 
             ("left", "◀", 35), ("down", "▼", 35), ("right", "▶", 35)]
        ]
        
        self.container_layout.setSpacing(5)
        for row in rows:
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(5)
            for key_id, label, width in row:
                if key_id is None:
                    # Spacer item
                    spacer = QWidget()
                    spacer.setFixedWidth(width)
                    row_layout.addWidget(spacer)
                else:
                    key = KeyCap(key_id, label)
                    key.setFixedWidth(width)
                    key.setFixedHeight(30)
                    row_layout.addWidget(key)
                    self.key_widgets[key_id] = key
            self.container_layout.addLayout(row_layout)

    def build_wasd_layout(self):
        # Compact, balanced and centered WASD gaming panel
        self.container_layout.setSpacing(6)
        
        # Row 1: W key centered
        r1 = QHBoxLayout()
        r1.setSpacing(6)
        r1.addStretch()
        w_key = KeyCap("w", "W")
        w_key.setFixedSize(45, 45)
        r1.addWidget(w_key)
        r1.addStretch()
        self.key_widgets["w"] = w_key
        
        # Row 2: A S D keys centered
        r2 = QHBoxLayout()
        r2.setSpacing(6)
        r2.addStretch()
        a_key = KeyCap("a", "A"); a_key.setFixedSize(45, 45)
        s_key = KeyCap("s", "S"); s_key.setFixedSize(45, 45)
        d_key = KeyCap("d", "D"); d_key.setFixedSize(45, 45)
        r2.addWidget(a_key)
        r2.addWidget(s_key)
        r2.addWidget(d_key)
        r2.addStretch()
        self.key_widgets["a"] = a_key
        self.key_widgets["s"] = s_key
        self.key_widgets["d"] = d_key
        
        # Row 3: Modifiers Shift, Space, Ctrl centered
        r3 = QHBoxLayout()
        r3.setSpacing(6)
        r3.addStretch()
        shift_key = KeyCap("shift_l", "Shift"); shift_key.setFixedSize(60, 30)
        space_key = KeyCap("space", "Space"); space_key.setFixedSize(130, 30)
        ctrl_key = KeyCap("ctrl_l", "Ctrl"); ctrl_key.setFixedSize(60, 30)
        r3.addWidget(shift_key)
        r3.addWidget(space_key)
        r3.addWidget(ctrl_key)
        r3.addStretch()
        
        self.key_widgets["shift_l"] = shift_key
        self.key_widgets["space"] = space_key
        self.key_widgets["ctrl_l"] = ctrl_key
        
        self.container_layout.addLayout(r1)
        self.container_layout.addLayout(r2)
        self.container_layout.addLayout(r3)

    def build_osu_layout(self):
        # Compact and centered Osu! rhythm keypad layout
        self.container_layout.setSpacing(8)
        
        # Row 1: ESC key
        r1 = QHBoxLayout()
        r1.addStretch()
        esc_key = KeyCap("esc", "ESC")
        esc_key.setFixedSize(60, 30)
        r1.addWidget(esc_key)
        r1.addStretch()
        self.key_widgets["esc"] = esc_key
        
        # Row 2: Z and X keys side by side
        r2 = QHBoxLayout()
        r2.setSpacing(12)
        r2.addStretch()
        z_key = KeyCap("z", "Z"); z_key.setFixedSize(55, 55)
        x_key = KeyCap("x", "X"); x_key.setFixedSize(55, 55)
        r2.addWidget(z_key)
        r2.addWidget(x_key)
        r2.addStretch()
        self.key_widgets["z"] = z_key
        self.key_widgets["x"] = x_key
        
        # Row 3: Space (for menu/combos)
        r3 = QHBoxLayout()
        r3.addStretch()
        space_key = KeyCap("space", "Space"); space_key.setFixedSize(140, 30)
        r3.addWidget(space_key)
        r3.addStretch()
        self.key_widgets["space"] = space_key
        
        self.container_layout.addLayout(r1)
        self.container_layout.addLayout(r2)
        self.container_layout.addLayout(r3)

    def build_dota_layout(self):
        # Dota 2 layout: Abilities, Sub-abilities, Items, Space, Esc
        self.container_layout.setSpacing(6)
        
        # Row 1: Esc + 1 2 3 4 5 6
        r1 = QHBoxLayout()
        r1.setContentsMargins(0, 0, 0, 0)
        r1.setSpacing(6)
        r1.addStretch()
        esc_key = KeyCap("esc", "ESC"); esc_key.setFixedSize(40, 30); r1.addWidget(esc_key)
        r1.addWidget(QWidget()) # divider spacer
        for num in ["1", "2", "3", "4", "5", "6"]:
            key = KeyCap(num, num); key.setFixedSize(35, 30); r1.addWidget(key)
            self.key_widgets[num] = key
        self.key_widgets["esc"] = esc_key
        r1.addStretch()
        
        # Row 2: Tab + Q W E R D F
        r2 = QHBoxLayout()
        r2.setContentsMargins(0, 0, 0, 0)
        r2.setSpacing(6)
        r2.addStretch()
        tab_key = KeyCap("tab", "Tab"); tab_key.setFixedSize(45, 40); r2.addWidget(tab_key)
        self.key_widgets["tab"] = tab_key
        for letter in ["q", "w", "e", "r", "d", "f"]:
            key = KeyCap(letter, letter.upper()); key.setFixedSize(40, 40); r2.addWidget(key)
            self.key_widgets[letter] = key
        r2.addStretch()
        
        # Row 3: Caps + Z X C V B N
        r3 = QHBoxLayout()
        r3.setContentsMargins(0, 0, 0, 0)
        r3.setSpacing(6)
        r3.addStretch()
        caps_key = KeyCap("caps_lock", "Caps"); caps_key.setFixedSize(55, 40); r3.addWidget(caps_key)
        self.key_widgets["caps_lock"] = caps_key
        for letter in ["z", "x", "c", "v", "b", "n"]:
            key = KeyCap(letter, letter.upper()); key.setFixedSize(40, 40); r3.addWidget(key)
            self.key_widgets[letter] = key
        r3.addStretch()
        
        # Row 4: Space + Ctrl + Alt
        r4 = QHBoxLayout()
        r4.setContentsMargins(0, 0, 0, 0)
        r4.setSpacing(6)
        r4.addStretch()
        ctrl_key = KeyCap("ctrl_l", "Ctrl"); ctrl_key.setFixedSize(65, 30); r4.addWidget(ctrl_key)
        alt_key = KeyCap("alt_l", "Alt"); alt_key.setFixedSize(55, 30); r4.addWidget(alt_key)
        space_key = KeyCap("space", "Space"); space_key.setFixedSize(180, 30); r4.addWidget(space_key)
        self.key_widgets["ctrl_l"] = ctrl_key
        self.key_widgets["alt_l"] = alt_key
        self.key_widgets["space"] = space_key
        r4.addStretch()
        
        self.container_layout.addLayout(r1)
        self.container_layout.addLayout(r2)
        self.container_layout.addLayout(r3)
        self.container_layout.addLayout(r4)

    def build_custom_layout(self):
        # Parses list of custom keys and displays them dynamically in a beautiful wrapped grid layout
        custom_keys_str = self.config.get("custom_layout_keys")
        keys = [k.strip().lower() for k in custom_keys_str.split(",") if k.strip()]
        if not keys:
            keys = ["q", "w", "e", "r"] # Default custom fallback
            
        self.container_layout.setSpacing(8)
        
        row_size = 8
        rows = [keys[i:i + row_size] for i in range(0, len(keys), row_size)]
        
        for row in rows:
            row_layout = QHBoxLayout()
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(8)
            row_layout.addStretch()
            for key_id in row:
                label = KEY_MAP_LABELS.get(key_id, key_id.upper())
                width = 40
                if key_id == "space":
                    width = 120
                elif key_id in ("shift_l", "shift_r", "enter", "backspace"):
                    width = 65
                elif key_id in ("ctrl_l", "ctrl_r", "alt_l", "alt_r", "tab", "caps_lock"):
                    width = 50
                    
                key = KeyCap(key_id, label)
                key.setFixedWidth(width)
                key.setFixedHeight(40) # Larger tactile keys
                row_layout.addWidget(key)
                self.key_widgets[key_id] = key
            row_layout.addStretch()
            self.container_layout.addLayout(row_layout)

    def build_pressed_layout(self):
        # A simple horizontal strip that scrolls key log items
        self.pressed_layout = QHBoxLayout()
        self.pressed_layout.setContentsMargins(5, 5, 5, 5)
        self.pressed_layout.setSpacing(8)
        self.pressed_layout.setAlignment(Qt.AlignCenter)
        self.container_layout.addLayout(self.pressed_layout)
        
        # Hint label
        hint = QLabel("Нажимайте клавиши...")
        hint.setStyleSheet("color: rgba(255,255,255,100); font-style: italic;")
        self.pressed_layout.addWidget(hint)
        self.key_widgets["__hint__"] = hint

    def add_pressed_key_history(self, key_name):
        """Pushes a key description label into the visual sliding layout (Pressed keys only)."""
        # Remove placeholder hint if any
        if "__hint__" in self.key_widgets:
            hint = self.key_widgets.pop("__hint__")
            hint.setParent(None)
            hint.deleteLater()
            
        theme = self.config.get("theme")
        accent = self.config.get("key_highlight_color")
        
        # Create key block
        display_label = key_name.upper()
        if key_name == "space":
            display_label = "SPACE"
            
        lbl = QLabel(display_label)
        lbl.setStyleSheet(get_overlay_key_qss(theme, accent, is_pressed=True))
        lbl.setContentsMargins(12, 6, 12, 6)
        lbl.setFixedHeight(30)
        
        # Create opacity effect for smooth fading
        opacity_effect = QGraphicsOpacityEffect(lbl)
        lbl.setGraphicsEffect(opacity_effect)
        opacity_effect.setOpacity(1.0)
        
        self.pressed_layout.addWidget(lbl)
        self.pressed_key_items.append((lbl, opacity_effect))
        
        # Fade out timer
        fade_timer = QTimer(self)
        fade_timer.setSingleShot(True)
        
        def start_fade(target_lbl=lbl, effect=opacity_effect):
            try:
                from shiboken6 import isValid
                if not isValid(target_lbl) or not isValid(effect):
                    return
                anim = QPropertyAnimation(effect, b"opacity")
                anim.setDuration(400)
                anim.setStartValue(1.0)
                anim.setEndValue(0.0)
                anim.finished.connect(lambda: self.remove_key_history_item(target_lbl))
                anim.start()
                # Cache animation reference to prevent early garbage collection
                target_lbl._fade_anim = anim
            except RuntimeError:
                pass
            
        fade_timer.timeout.connect(start_fade)
        fade_timer.start(1000) # Start fading after 1s
        
        # Cap queue limit to 6 elements
        if len(self.pressed_key_items) > 6:
            old_lbl, _ = self.pressed_key_items.pop(0)
            self.remove_key_history_item(old_lbl)

    def remove_key_history_item(self, widget):
        """Cleanly removes a key history element from display."""
        # Find item in tracker
        self.pressed_key_items = [(w, e) for w, e in self.pressed_key_items if w != widget]
        widget.setParent(None)
        widget.deleteLater()
        
        # Put hint back if empty
        if not self.pressed_key_items and "__hint__" not in self.key_widgets:
            hint = QLabel("Нажимайте клавиши...")
            hint.setStyleSheet("color: rgba(255,255,255,100); font-style: italic;")
            self.pressed_layout.addWidget(hint)
            self.key_widgets["__hint__"] = hint

    def check_fullscreen_and_topmost(self):
        """Detects if the foreground window is in exclusive fullscreen and maintains topmost state."""
        if not self.config.get("overlay_enabled"):
            return

        try:
            user32 = ctypes.windll.user32
            hwnd_foreground = user32.GetForegroundWindow()
            if not hwnd_foreground:
                return

            # Skip checking if foreground is our own window
            hwnd_self = int(self.winId())
            if hwnd_foreground == hwnd_self:
                return
                
            # Skip if settings window is active
            length = user32.GetWindowTextLengthW(hwnd_foreground)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd_foreground, buf, length + 1)
            title = buf.value
            if "KeySound Overlay" in title:
                return

            # Check dimensions of foreground window
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_int), ("top", ctypes.c_int), 
                            ("right", ctypes.c_int), ("bottom", ctypes.c_int)]
            rect = RECT()
            user32.GetWindowRect(hwnd_foreground, ctypes.byref(rect))
            fw_width = rect.right - rect.left
            fw_height = rect.bottom - rect.top

            # Get primary screen resolution
            from PySide6.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            if screen:
                geom = screen.geometry()
                sw, sh = geom.width(), geom.height()
                
                # If active window is fullscreen and not wallpaper/explorer
                if fw_width >= sw and fw_height >= sh:
                    if self.isVisible():
                        self.hide_due_to_fullscreen = True
                        super().hide()
                    return

            # If not fullscreen, restore visibility if we hid it
            if getattr(self, "hide_due_to_fullscreen", False):
                self.hide_due_to_fullscreen = False
                super().show()

            # Maintain topmost state by resetting window flag if necessary
            if self.isVisible() and not self.config.get("overlay_unlocked"):
                user32.SetWindowPos(hwnd_self, -1, 0, 0, 0, 0, 0x0013) # SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE
        except Exception as e:
            print(f"Error in fullscreen/topmost check: {e}")

    # OVERLAY INTERACTION / DRAG HANDLING
    def mousePressEvent(self, event):
        if self.config.get("overlay_unlocked") and event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.config.get("overlay_unlocked") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.config.get("overlay_unlocked"):
            self.config.set("overlay_x", self.x())
            self.config.set("overlay_y", self.y())
            event.accept()


class MouseWidget(QFrame):
    """Visualizes global mouse movement, button clicks, and scrolling."""
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.mouse_pos = (0, 0)
        self.pressed_buttons = set()
        self.scroll_indicator = 0  # 1 for up, -1 for down, 0 for idle
        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.reset_scroll)
        self.setObjectName("MouseWidget")
        self.setFixedSize(80, 130)

    def reset_scroll(self):
        self.scroll_indicator = 0
        self.update()

    def set_mouse_position(self, x, y):
        self.mouse_pos = (x, y)
        if self.config.get("mouse_overlay_show_coords"):
            self.update()

    def set_button_state(self, button_name, is_pressed):
        if is_pressed:
            self.pressed_buttons.add(button_name)
        else:
            self.pressed_buttons.discard(button_name)
        self.update()

    def set_scroll(self, direction):
        self.scroll_indicator = direction
        self.update()
        self.scroll_timer.start(150) # Reset highlighting after 150ms

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        theme = self.config.get("theme").lower()
        accent_str = self.config.get("key_highlight_color")
        accent_color = QColor(accent_str)
        
        # Idle colors based on active theme
        if theme == "light":
            bg_body = QColor(220, 220, 220, 150)
            border_body = QColor(180, 180, 180, 255)
            text_color = QColor(28, 28, 28)
            idle_btn = QColor(240, 240, 240, 150)
        elif theme == "glass":
            bg_body = QColor(45, 45, 45, 120)
            border_body = QColor(255, 255, 255, 50)
            text_color = QColor(255, 255, 255)
            idle_btn = QColor(70, 70, 70, 100)
        elif theme == "neon":
            bg_body = QColor(11, 21, 40, 100)
            border_body = QColor(0, 85, 100, 150)
            text_color = QColor(0, 240, 255)
            idle_btn = QColor(20, 35, 60, 100)
            accent_color = QColor(0, 240, 255)
        else: # dark / custom
            # Try parsing custom values from register
            from app.themes import CUSTOM_THEMES
            if theme in CUSTOM_THEMES:
                t_overlay = CUSTOM_THEMES[theme].get("overlay", {})
                # Idle settings
                bg_body = QColor(t_overlay.get("key_idle_bg", "#2D2D2D"))
                border_body = QColor(t_overlay.get("key_idle_border", "#3D3D3D"))
                text_color = QColor(t_overlay.get("key_idle_text", "#FFFFFF"))
                idle_btn = QColor(bg_body.red(), bg_body.green(), bg_body.blue(), 100)
                accent_color = QColor(t_overlay.get("key_active_bg", accent_str))
            else:
                bg_body = QColor(50, 50, 50, 180)
                border_body = QColor(70, 70, 70, 255)
                text_color = QColor(226, 226, 226)
                idle_btn = QColor(60, 60, 60, 180)

        # Draw Mouse Shape (Centered in widget)
        mx, my, mw, mh = 8, 5, 64, 96
        
        # Mouse Background
        painter.setBrush(QBrush(bg_body))
        painter.setPen(QPen(border_body, 1.5))
        painter.drawRoundedRect(mx, my, mw, mh, 16, 16)
        
        # Split line for buttons (upper half)
        btn_height = 42
        painter.setPen(QPen(border_body, 1))
        painter.drawLine(mx + mw // 2, my, mx + mw // 2, my + btn_height)
        painter.drawLine(mx, my + btn_height, mx + mw, my + btn_height)

        # Highlight Left Click
        if "left" in self.pressed_buttons:
            painter.setBrush(QBrush(accent_color))
            painter.setPen(Qt.NoPen)
            painter.save()
            painter.setClipRect(mx, my, mw // 2, btn_height)
            painter.drawRoundedRect(mx, my, mw, mh, 16, 16)
            painter.restore()

        # Highlight Right Click
        if "right" in self.pressed_buttons:
            painter.setBrush(QBrush(accent_color))
            painter.setPen(Qt.NoPen)
            painter.save()
            painter.setClipRect(mx + mw // 2, my, mw // 2, btn_height)
            painter.drawRoundedRect(mx, my, mw, mh, 16, 16)
            painter.restore()

        # Draw Scroll Wheel
        wx, wy, ww, wh = mx + mw // 2 - 4, my + 12, 8, 18
        if "middle" in self.pressed_buttons or self.scroll_indicator != 0:
            painter.setBrush(QBrush(accent_color if "middle" in self.pressed_buttons else QColor(text_color)))
            if theme == "neon":
                painter.setPen(QPen(QColor(0, 240, 255), 1))
            else:
                painter.setPen(Qt.NoPen)
        else:
            painter.setBrush(QBrush(text_color))
            painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(wx, wy, ww, wh, 2, 2)
        
        # Scroll wheel arrow indicator
        if self.scroll_indicator != 0:
            painter.setPen(QPen(text_color, 1))
            if self.scroll_indicator > 0: # Up arrow
                painter.drawLine(wx + 4, wy - 4, wx + 1, wy - 1)
                painter.drawLine(wx + 4, wy - 4, wx + 7, wy - 1)
            else: # Down arrow
                painter.drawLine(wx + 4, wy + wh + 4, wx + 1, wy + wh + 1)
                painter.drawLine(wx + 4, wy + wh + 4, wx + 7, wy + wh + 1)

        # Side Buttons (X1, X2) on the left side
        s_height = 18
        s_y1 = my + 50
        s_y2 = s_y1 + 22
        
        # X1
        if "x1" in self.pressed_buttons:
            painter.setBrush(QBrush(accent_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(mx - 3, s_y1, 4, s_height, 1, 1)
        else:
            painter.setBrush(QBrush(idle_btn))
            painter.setPen(QPen(border_body, 0.5))
            painter.drawRoundedRect(mx - 2, s_y1, 2, s_height, 1, 1)
            
        # X2
        if "x2" in self.pressed_buttons:
            painter.setBrush(QBrush(accent_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(mx - 3, s_y2, 4, s_height, 1, 1)
        else:
            painter.setBrush(QBrush(idle_btn))
            painter.setPen(QPen(border_body, 0.5))
            painter.drawRoundedRect(mx - 2, s_y2, 2, s_height, 1, 1)

        # Draw Coordinates X / Y
        if self.config.get("mouse_overlay_show_coords"):
            painter.setPen(QPen(text_color))
            font = QFont("Segoe UI", 9)
            font.setBold(True)
            painter.setFont(font)
            
            x_str = f"X: {self.mouse_pos[0]}"
            y_str = f"Y: {self.mouse_pos[1]}"
            painter.drawText(0, my + mh + 14, 80, 15, Qt.AlignCenter, x_str)
            painter.drawText(0, my + mh + 26, 80, 15, Qt.AlignCenter, y_str)


class MouseOverlayWindow(QWidget):
    """Standalone transparent window displaying only the visual MouseWidget."""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.drag_position = QPoint()
        self.hide_due_to_fullscreen = False
        
        # Window attributes setup
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setMouseTracking(True)
        
        # Create container QFrame
        self.container = QFrame(self)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(4, 4, 4, 4)
        self.container.setObjectName("MouseContainerFrame")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.container)
        
        self.mouse_widget = MouseWidget(self.config, self)
        self.container_layout.addWidget(self.mouse_widget, 0, Qt.AlignCenter)
        
        self.reload_ui()
        
        # Timer for keeping topmost and auto-hiding under exclusive fullscreen games
        self.fullscreen_timer = QTimer(self)
        self.fullscreen_timer.timeout.connect(self.check_fullscreen_and_topmost)
        self.fullscreen_timer.start(1000)

    def reload_ui(self):
        w, h = 90, 140
        x = self.config.get("mouse_overlay_x")
        y = self.config.get("mouse_overlay_y")
        self.setGeometry(x, y, w, h)
        self.setFixedSize(w, h)
        
        self.update_click_through_state()
        self.update()

    def update_click_through_state(self):
        """Toggles window interaction click-through based on settings."""
        unlocked = self.config.get("mouse_overlay_unlocked")
        hwnd = int(self.winId())
        set_click_through(hwnd, not unlocked)
        
        accent = self.config.get("key_highlight_color")
        theme = self.config.get("theme").lower()
        opacity = self.config.get("mouse_overlay_opacity")
        alpha = int(opacity * 180)
        
        if unlocked:
            self.container.setStyleSheet(f"""
                QFrame#MouseContainerFrame {{
                    border: 2px dashed {accent};
                    background-color: rgba(20, 20, 20, 160);
                    border-radius: 8px;
                }}
            """)
        else:
            from app.themes import CUSTOM_THEMES
            if theme in CUSTOM_THEMES:
                t_overlay = CUSTOM_THEMES[theme].get("overlay", {})
                bg = t_overlay.get("container_bg", f"rgba(20, 20, 20, {alpha})")
                border = t_overlay.get("container_border", "none")
                border_str = f"border: 1px solid {border};" if border != "none" else "border: none;"
                self.container.setStyleSheet(f"""
                    QFrame#MouseContainerFrame {{
                        {border_str}
                        background-color: {bg};
                        border-radius: 8px;
                    }}
                """)
            elif theme == "light":
                self.container.setStyleSheet(f"""
                    QFrame#MouseContainerFrame {{
                        border: none;
                        background-color: rgba(240, 240, 240, {alpha});
                        border-radius: 8px;
                    }}
                """)
            elif theme == "glass":
                border_alpha = int(opacity * 30)
                self.container.setStyleSheet(f"""
                    QFrame#MouseContainerFrame {{
                        border: 1px solid rgba(255, 255, 255, {border_alpha});
                        background-color: rgba(25, 25, 25, {int(opacity * 110)});
                        border-radius: 8px;
                    }}
                """)
            elif theme == "neon":
                border_alpha = int(opacity * 60)
                self.container.setStyleSheet(f"""
                    QFrame#MouseContainerFrame {{
                        border: 1px solid rgba(0, 240, 255, {border_alpha});
                        background-color: rgba(5, 8, 17, {alpha});
                        border-radius: 8px;
                    }}
                """)
            else: # dark
                self.container.setStyleSheet(f"""
                    QFrame#MouseContainerFrame {{
                        border: none;
                        background-color: rgba(20, 20, 20, {alpha});
                        border-radius: 8px;
                    }}
                """)

    def check_fullscreen_and_topmost(self):
        if not self.config.get("mouse_overlay_enabled"):
            return
            
        try:
            user32 = ctypes.windll.user32
            hwnd_foreground = user32.GetForegroundWindow()
            if not hwnd_foreground:
                return

            hwnd_self = int(self.winId())
            if hwnd_foreground == hwnd_self:
                return

            # Check if settings window or other keysound windows are active
            length = user32.GetWindowTextLengthW(hwnd_foreground)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd_foreground, buf, length + 1)
            title = buf.value
            if "KeySound Overlay" in title:
                return

            # Exclusive fullscreen check
            class RECT(ctypes.Structure):
                _fields_ = [("left", ctypes.c_int), ("top", ctypes.c_int), 
                            ("right", ctypes.c_int), ("bottom", ctypes.c_int)]
            rect = RECT()
            user32.GetWindowRect(hwnd_foreground, ctypes.byref(rect))
            fw_width = rect.right - rect.left
            fw_height = rect.bottom - rect.top

            from PySide6.QtWidgets import QApplication
            screen = QApplication.primaryScreen()
            if screen:
                geom = screen.geometry()
                sw, sh = geom.width(), geom.height()
                if fw_width >= sw and fw_height >= sh:
                    if self.isVisible():
                        self.hide_due_to_fullscreen = True
                        super().hide()
                    return

            if getattr(self, "hide_due_to_fullscreen", False):
                self.hide_due_to_fullscreen = False
                super().show()

            # Keep topmost
            if self.isVisible() and not self.config.get("mouse_overlay_unlocked"):
                user32.SetWindowPos(hwnd_self, -1, 0, 0, 0, 0, 0x0013)
        except Exception as e:
            print(f"Error in mouse fullscreen topmost check: {e}")

    # Drag & Drop functionality
    def mousePressEvent(self, event):
        if self.config.get("mouse_overlay_unlocked") and event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.config.get("mouse_overlay_unlocked") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.config.get("mouse_overlay_unlocked"):
            pos = self.pos()
            self.config.set("mouse_overlay_x", pos.x())
            self.config.set("mouse_overlay_y", pos.y())
            event.accept()

    def set_mouse_position(self, x, y):
        if self.mouse_widget:
            self.mouse_widget.set_mouse_position(x, y)

    def set_mouse_button_state(self, button_name, is_pressed):
        if self.mouse_widget:
            self.mouse_widget.set_button_state(button_name, is_pressed)

    def set_mouse_scroll(self, direction):
        if self.mouse_widget:
            self.mouse_widget.set_scroll(direction)

