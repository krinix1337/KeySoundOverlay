# app/overlay_window.py
import ctypes
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPoint, QTimer, QPropertyAnimation
from PySide6.QtGui import QColor
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

    # OVERLAY INTERACTION / DRAG HANDLING
    def mousePressEvent(self, event):
        if self.config.get("overlay_unlocked") and event.button() == Qt.LeftButton:
            # globalPosition() returns a QPointF, map to standard QPoint
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.config.get("overlay_unlocked") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if self.config.get("overlay_unlocked"):
            # Update coordinate configuration
            self.config.set("overlay_x", self.x())
            self.config.set("overlay_y", self.y())
            event.accept()
