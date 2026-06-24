# app/profiles.py
import os
import json


class ProfileManager:
    """Manages named settings profiles stored as JSON files."""

    def __init__(self, app_data_dir):
        self.profiles_dir = os.path.join(app_data_dir, "profiles")
        os.makedirs(self.profiles_dir, exist_ok=True)

    def list_profiles(self):
        """Returns a sorted list of profile names (without .json extension)."""
        try:
            files = [
                f[:-5] for f in os.listdir(self.profiles_dir)
                if f.endswith(".json")
            ]
            return sorted(files)
        except Exception:
            return []

    def save_profile(self, name, settings: dict):
        """Saves a settings dict as a named profile. Returns True on success."""
        if not name or not name.strip():
            return False
        safe_name = self._sanitize(name)
        path = os.path.join(self.profiles_dir, f"{safe_name}.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"profile_display_name": name, "settings": settings}, f,
                          indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"ProfileManager: error saving profile '{name}': {e}")
            return False

    def load_profile(self, name):
        """Loads and returns a settings dict for the given profile name.
        Returns None if not found or invalid."""
        safe_name = self._sanitize(name)
        path = os.path.join(self.profiles_dir, f"{safe_name}.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("settings", None)
        except Exception as e:
            print(f"ProfileManager: error loading profile '{name}': {e}")
            return None

    def delete_profile(self, name):
        """Deletes a profile file. Returns True on success."""
        safe_name = self._sanitize(name)
        path = os.path.join(self.profiles_dir, f"{safe_name}.json")
        try:
            if os.path.exists(path):
                os.remove(path)
                return True
        except Exception as e:
            print(f"ProfileManager: error deleting profile '{name}': {e}")
        return False

    def get_display_name(self, name):
        """Returns the display name stored inside the profile JSON."""
        safe_name = self._sanitize(name)
        path = os.path.join(self.profiles_dir, f"{safe_name}.json")
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return data.get("profile_display_name", name)
        except Exception:
            pass
        return name

    @staticmethod
    def _sanitize(name: str) -> str:
        """Converts a profile display name to a safe filename slug."""
        import re
        slug = re.sub(r'[^\w\s-]', '', name.strip()).strip()
        slug = re.sub(r'[\s]+', '_', slug)
        return slug[:64] or "profile"
