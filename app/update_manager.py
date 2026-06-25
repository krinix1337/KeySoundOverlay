# app/update_manager.py
import os
import sys
import re
import urllib.request
import json
from PySide6.QtCore import QThread, Signal

CURRENT_VERSION = "1.5.0"
DEFAULT_GITHUB_REPO = "krinix1337/KeySoundOverlay"  # Fallback repository path

def get_github_repo():
    """Parses local .git/config to determine the repository owner and name dynamically."""
    if getattr(sys, 'frozen', False):
        return DEFAULT_GITHUB_REPO
    try:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        git_config_path = os.path.join(base_dir, ".git", "config")
        if os.path.exists(git_config_path):
            with open(git_config_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Match HTTPS and SSH Github URLs
            match = re.search(r'url\s*=\s*(?:https://github\.com/|git@github\.com:)([^/\s]+)/([^/\s\.\n\r]+)(?:\.git)?', content)
            if match:
                owner = match.group(1)
                repo = match.group(2).strip()
                return f"{owner}/{repo}"
    except Exception as e:
        print(f"Error parsing .git/config: {e}")
    return DEFAULT_GITHUB_REPO

def parse_version(v_str):
    """Normalizes and parses a version string (e.g. 'v1.2.3-beta' -> [1, 2, 3])."""
    clean = re.sub(r'[^\d\.]', '', v_str)
    try:
        parts = [int(x) for x in clean.split('.') if x]
        return parts[:3]  # Only major.minor.patch
    except Exception:
        return [0, 0, 0]

def is_newer_version(latest_str, current_str):
    """Compares semver versions; returns True if latest_str is newer than current_str."""
    latest_parts = parse_version(latest_str)
    current_parts = parse_version(current_str)
    
    max_len = max(len(latest_parts), len(current_parts))
    latest_parts += [0] * (max_len - len(latest_parts))
    current_parts += [0] * (max_len - len(current_parts))
    
    return latest_parts > current_parts

class UpdateCheckerWorker(QThread):
    # Signals:
    # (update_available, version_tag, changelog_text, download_url)
    check_finished = Signal(bool, str, str, str)
    check_failed = Signal(str)

    def __init__(self, repo_path=None):
        super().__init__()
        self.repo_path = repo_path or get_github_repo()

    def run(self):
        try:
            url = f"https://api.github.com/repos/{self.repo_path}/releases/latest"
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'KeySoundOverlay-Updater'}
            )
            with urllib.request.urlopen(req, timeout=8) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            latest_version = data.get("tag_name", "0.0.0")
            changelog = data.get("body", "No description provided.")
            
            # Find the setup installer asset (.exe)
            download_url = ""
            assets = data.get("assets", [])
            for asset in assets:
                name = asset.get("name", "")
                if name.endswith(".exe") or "setup" in name.lower():
                    download_url = asset.get("browser_download_url", "")
                    break
            
            if not download_url and assets:
                download_url = assets[0].get("browser_download_url", "")

            update_available = is_newer_version(latest_version, CURRENT_VERSION)
            self.check_finished.emit(update_available, latest_version, changelog, download_url)
            
        except Exception as e:
            self.check_failed.emit(str(e))


class FileDownloaderWorker(QThread):
    progress = Signal(int)       # Percent completed (0-100)
    finished = Signal(str)       # Local file path
    failed = Signal(str)         # Error message

    def __init__(self, url, dest_path):
        super().__init__()
        self.url = url
        self.dest_path = dest_path

    def run(self):
        try:
            req = urllib.request.Request(
                self.url,
                headers={'User-Agent': 'KeySoundOverlay-Updater'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                meta = response.info()
                content_length = meta.get("Content-Length")
                total_size = int(content_length) if content_length else 0
                
                bytes_downloaded = 0
                block_size = 8192
                
                with open(self.dest_path, "wb") as f:
                    while True:
                        buffer = response.read(block_size)
                        if not buffer:
                            break
                        f.write(buffer)
                        bytes_downloaded += len(buffer)
                        
                        if total_size > 0:
                            percent = int((bytes_downloaded / total_size) * 100)
                            self.progress.emit(percent)
                            
            self.progress.emit(100)
            self.finished.emit(self.dest_path)
        except Exception as e:
            self.failed.emit(str(e))
