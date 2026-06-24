import os
import json

DEFAULT_SETTINGS = {
    "sound_enabled": True,
    "sound_file": "",  # Empty string means default click
    "volume": 80,
    "pitch_randomize": True,
    "repeat_on_hold": False,
    "overlay_enabled": True,
    "overlay_unlocked": False,
    "overlay_opacity": 0.85,
    "overlay_scale": 1.0,
    "overlay_mode": "full",  # "full", "wasd", "pressed"
    "theme": "dark",        # "dark", "light", "glass", "neon"
    "key_highlight_color": "#0078D4",
    "autostart": False,
    "minimize_to_tray": True,
    "start_minimized": False,
    "custom_layout_keys": "q, w, e, r, d, f, space",
    "overlay_x": 100,
    "overlay_y": 600,
    "overlay_width": 800,
    "overlay_height": 260,
    
    # Mouse Overlay Settings
    "mouse_overlay_enabled": True,
    "mouse_overlay_show_coords": True,
    "mouse_overlay_show_clicks": True,
    "mouse_overlay_unlocked": False,
    "mouse_overlay_x": 720,
    "mouse_overlay_y": 600,
    "mouse_overlay_opacity": 0.85,
    
    # Fullscreen & Updates
    "show_in_fullscreen": False,
    "check_updates_on_startup": True,
    "key_press_animation": True,
}

class AppConfig:
    def __init__(self):
        self.app_data_dir = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "KeySoundOverlay")
        self.config_path = os.path.join(self.app_data_dir, "settings.json")
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        """Loads configuration from JSON file."""
        if not os.path.exists(self.app_data_dir):
            try:
                os.makedirs(self.app_data_dir)
            except Exception:
                # If APPDATA write fails, fallback to local directory
                self.app_data_dir = "."
                self.config_path = "settings.json"

        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded_data = json.load(f)
                    # Merge loaded data with defaults to handle version updates
                    for key, val in loaded_data.items():
                        if key in DEFAULT_SETTINGS:
                            self.settings[key] = val
            except Exception as e:
                print(f"Error loading configuration: {e}")
                self.settings = DEFAULT_SETTINGS.copy()
        else:
            self.save()

    def save(self):
        """Saves current configuration to JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving configuration: {e}")

    def get(self, key, default=None):
        return self.settings.get(key, DEFAULT_SETTINGS.get(key, default))

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def reset(self):
        """Resets configurations to defaults."""
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()
