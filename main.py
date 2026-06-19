# main.py
import sys
import os
from PySide6.QtWidgets import QApplication
from app.config import AppConfig
from app.sound_player import SoundPlayer
from app.overlay_window import OverlayWindow
from app.settings_window import SettingsWindow
from app.tray import SystemTrayController
from app.keyboard_listener import GlobalKeyboardListener

from PySide6.QtCore import QLockFile, QDir

def main():
    # Initialize PySide6 Application
    app = QApplication(sys.argv)
    
    # Prevent multiple instances running concurrently using QLockFile and QSharedMemory
    lock_file = QLockFile(os.path.join(QDir.tempPath(), "keysound_overlay.lock"))
    if not lock_file.tryLock(100):
        print("KeySound Overlay is already running (detected via lock file).")
        sys.exit(0)
        
    from PySide6.QtCore import QSharedMemory
    shared_mem = QSharedMemory("keysound_overlay_unique_shared_memory_key")
    if not shared_mem.create(1):
        print("KeySound Overlay is already running (detected via shared memory).")
        sys.exit(0)
        
    # Keep references on the app object to prevent garbage collection
    app.lock_file = lock_file
    app.shared_mem = shared_mem
        
    # CRITICAL: Prevent application from quitting when settings window is hidden
    app.setQuitOnLastWindowClosed(False)
    
    # Load configuration
    config = AppConfig()
    
    # Initialize low-latency sound player
    sound_player = SoundPlayer(config)
    
    # Initialize overlay window
    overlay_window = OverlayWindow(config, sound_player)
    
    # Initialize settings window
    settings_window = SettingsWindow(config, sound_player)
    
    # Initialize system tray controller
    tray_controller = SystemTrayController(app, config, settings_window, overlay_window)
    tray_controller.show()
    
    # Initialize global keyboard listener
    listener = GlobalKeyboardListener(config)
    
    # Connect global keyboard signals to overlay window
    # The listener runs in a separate thread; PySide6 signals handle cross-thread communication safely
    listener.key_pressed.connect(lambda key: overlay_window.set_key_state(key, True))
    listener.key_released.connect(lambda key: overlay_window.set_key_state(key, False))
    
    # Connect Settings Window actions
    def on_settings_changed():
        if config.get("overlay_enabled"):
            overlay_window.show()
        else:
            overlay_window.hide()
        overlay_window.reload_ui()
        
    settings_window.settings_changed.connect(on_settings_changed)
    
    def reset_overlay_position():
        config.set("overlay_x", 100)
        config.set("overlay_y", 600)
        config.set("overlay_width", 800)
        config.set("overlay_height", 260)
        overlay_window.reload_ui()
        
    settings_window.reset_overlay_position_triggered.connect(reset_overlay_position)
    
    # Apply initial overlay display state
    if config.get("overlay_enabled"):
        overlay_window.show()
    else:
        overlay_window.hide()
        
    # Apply initial settings window display state
    if not config.get("start_minimized"):
        settings_window.show()
        
    # Start the global keyboard hook
    listener.start()
    
    try:
        # Run standard Qt event loop
        sys.exit(app.exec())
    finally:
        # Make sure keyboard hook thread exits cleanly when application closes
        listener.stop()

if __name__ == "__main__":
    main()
