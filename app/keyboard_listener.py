# app/keyboard_listener.py
from PySide6.QtCore import QObject, Signal
from pynput import keyboard

# VK Code to standard overlay key names
VK_MAP = {
    27: "esc",
    112: "f1", 113: "f2", 114: "f3", 115: "f4", 116: "f5", 117: "f6",
    118: "f7", 119: "f8", 120: "f9", 121: "f10", 122: "f11", 123: "f12",
    
    192: "`", 49: "1", 50: "2", 51: "3", 52: "4", 53: "5", 54: "6",
    55: "7", 56: "8", 57: "9", 48: "0", 189: "-", 187: "=", 8: "backspace",
    
    9: "tab", 81: "q", 87: "w", 69: "e", 82: "r", 84: "t", 89: "y",
    85: "u", 73: "i", 79: "o", 80: "p", 219: "[", 221: "]", 220: "\\",
    
    20: "caps_lock", 65: "a", 83: "s", 68: "d", 70: "f", 71: "g", 72: "h",
    74: "j", 75: "k", 76: "l", 186: ";", 222: "'", 13: "enter",
    
    160: "shift_l", 161: "shift_r", 16: "shift_l",  # General Shift maps to Shift L
    90: "z", 88: "x", 67: "c", 86: "v", 66: "b", 78: "n", 77: "m",
    188: ",", 190: ".", 191: "/",
    
    162: "ctrl_l", 163: "ctrl_r", 17: "ctrl_l",
    91: "win", 92: "win_r",
    164: "alt_l", 165: "alt_r", 18: "alt_l",
    32: "space",
    
    # Arrows and Navigation
    37: "left", 38: "up", 39: "right", 40: "down",
    45: "insert", 46: "delete", 36: "home", 35: "end", 33: "page_up", 34: "page_down",
    
    # Numpad
    96: "num_0", 97: "num_1", 98: "num_2", 99: "num_3", 100: "num_4",
    101: "num_5", 102: "num_6", 103: "num_7", 104: "num_8", 105: "num_9",
    106: "num_mul", 107: "num_add", 109: "num_sub", 110: "num_dec", 111: "num_div",
    144: "num_lock"
}

# Enum key names to standard overlay names
KEY_ENUM_MAP = {
    keyboard.Key.esc: "esc",
    keyboard.Key.f1: "f1", keyboard.Key.f2: "f2", keyboard.Key.f3: "f3", keyboard.Key.f4: "f4",
    keyboard.Key.f5: "f5", keyboard.Key.f6: "f6", keyboard.Key.f7: "f7", keyboard.Key.f8: "f8",
    keyboard.Key.f9: "f9", keyboard.Key.f10: "f10", keyboard.Key.f11: "f11", keyboard.Key.f12: "f12",
    keyboard.Key.tab: "tab",
    keyboard.Key.caps_lock: "caps_lock",
    keyboard.Key.shift: "shift_l",
    keyboard.Key.shift_l: "shift_l",
    keyboard.Key.shift_r: "shift_r",
    keyboard.Key.ctrl: "ctrl_l",
    keyboard.Key.ctrl_l: "ctrl_l",
    keyboard.Key.ctrl_r: "ctrl_r",
    keyboard.Key.alt: "alt_l",
    keyboard.Key.alt_l: "alt_l",
    keyboard.Key.alt_r: "alt_r",
    keyboard.Key.cmd: "win",
    keyboard.Key.cmd_r: "win_r",
    keyboard.Key.space: "space",
    keyboard.Key.enter: "enter",
    keyboard.Key.backspace: "backspace",
    keyboard.Key.left: "left",
    keyboard.Key.up: "up",
    keyboard.Key.right: "right",
    keyboard.Key.down: "down",
    keyboard.Key.insert: "insert",
    keyboard.Key.delete: "delete",
    keyboard.Key.home: "home",
    keyboard.Key.end: "end",
    keyboard.Key.page_up: "page_up",
    keyboard.Key.page_down: "page_down",
}

def resolve_key_name(key):
    """Translates a pynput key object into a standardized, layout-agnostic string identifier."""
    # Check if the key is in our Key Enum map
    if key in KEY_ENUM_MAP:
        return KEY_ENUM_MAP[key]
        
    # Attempt to resolve via virtual key code (vk) to circumvent active keyboard layouts
    vk = None
    if hasattr(key, 'vk') and key.vk is not None:
        vk = key.vk
    elif hasattr(key, 'value') and hasattr(key.value, 'vk') and key.value.vk is not None:
        vk = key.value.vk
        
    if vk is not None and vk in VK_MAP:
        return VK_MAP[vk]
        
    # Fallbacks
    if hasattr(key, 'char') and key.char:
        return key.char.lower()
        
    if hasattr(key, 'name') and key.name:
        return key.name.lower()
        
    # Final cleanup string representation
    k_str = str(key).replace("Key.", "").lower()
    if k_str.startswith("'") and k_str.endswith("'"):
        k_str = k_str[1:-1]
    return k_str

class GlobalKeyboardListener(QObject):
    key_pressed = Signal(str)    # Emits key code name on KeyDown
    key_released = Signal(str)   # Emits key code name on KeyUp

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.listener = None
        self.pressed_keys = set()

    def start(self):
        """Starts the global keyboard hook listener."""
        if self.listener is None:
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release,
                suppress=False  # Do not block keys, just spy on events
            )
            self.listener.daemon = True
            self.listener.start()

    def stop(self):
        """Stops the global keyboard hook listener."""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
        self.pressed_keys.clear()

    def _on_press(self, key):
        key_name = resolve_key_name(key)
        if not key_name:
            return

        repeat_on_hold = self.config.get("repeat_on_hold")
        
        if key_name in self.pressed_keys:
            # If repeating is disabled, ignore auto-generated keypress events on hold
            if not repeat_on_hold:
                return
        else:
            self.pressed_keys.add(key_name)
            
        self.key_pressed.emit(key_name)

    def _on_release(self, key):
        key_name = resolve_key_name(key)
        if not key_name:
            return

        if key_name in self.pressed_keys:
            self.pressed_keys.discard(key_name)
            
        self.key_released.emit(key_name)
