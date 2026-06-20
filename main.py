# main.py
import sys
import os
from PySide6.QtWidgets import QApplication
from app.config import AppConfig
from app.sound_player import SoundPlayer
from app.overlay_window import OverlayWindow, MouseOverlayWindow
from app.settings_window import SettingsWindow
from app.tray import SystemTrayController
from app.keyboard_listener import GlobalKeyboardListener
from app.mouse_listener import GlobalMouseListener
from app.update_manager import UpdateCheckerWorker
from app.update_dialog import UpdateDialog

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
    
    # Initialize overlay windows
    overlay_window = OverlayWindow(config, sound_player)
    mouse_overlay_window = MouseOverlayWindow(config)
    
    # Initialize settings window
    settings_window = SettingsWindow(config, sound_player)
    
    # Initialize system tray controller
    tray_controller = SystemTrayController(app, config, settings_window, overlay_window, mouse_overlay_window)
    tray_controller.show()
    
    # Initialize global keyboard listener
    listener = GlobalKeyboardListener(config)
    listener.key_pressed.connect(lambda key: overlay_window.set_key_state(key, True))
    listener.key_released.connect(lambda key: overlay_window.set_key_state(key, False))
    listener.start()
    
    # Initialize global mouse listener
    mouse_listener = GlobalMouseListener(config)
    mouse_listener.mouse_moved.connect(mouse_overlay_window.set_mouse_position)
    mouse_listener.mouse_clicked.connect(mouse_overlay_window.set_mouse_button_state)
    mouse_listener.mouse_scrolled.connect(mouse_overlay_window.set_mouse_scroll)
    mouse_listener.start()
    
    # Connect Settings Window actions
    def on_settings_changed():
        if config.get("overlay_enabled"):
            overlay_window.show()
        else:
            overlay_window.hide()
            
        if config.get("mouse_overlay_enabled"):
            mouse_overlay_window.show()
        else:
            mouse_overlay_window.hide()
            
        overlay_window.reload_ui()
        mouse_overlay_window.reload_ui()
        settings_window.apply_theme_styling()
        
    settings_window.settings_changed.connect(on_settings_changed)
    
    def reset_overlay_position():
        config.set("overlay_x", 100)
        config.set("overlay_y", 600)
        config.set("overlay_width", 800)
        config.set("overlay_height", 260)
        config.set("mouse_overlay_x", 720)
        config.set("mouse_overlay_y", 600)
        overlay_window.reload_ui()
        mouse_overlay_window.reload_ui()
        
    settings_window.reset_overlay_position_triggered.connect(reset_overlay_position)
    
    # Apply initial overlay display state
    if config.get("overlay_enabled"):
        overlay_window.show()
    else:
        overlay_window.hide()
        
    if config.get("mouse_overlay_enabled"):
        mouse_overlay_window.show()
    else:
        mouse_overlay_window.hide()
        
    # Apply initial settings window display state
    if not config.get("start_minimized"):
        settings_window.show()
        
    # Start update checker in the background (asynchronously)
    update_checker = UpdateCheckerWorker()
    
    def on_update_checked(update_available, latest_version, changelog, download_url):
        if update_available:
            update_dlg = UpdateDialog(config, settings_window)
            update_dlg.set_update_info(latest_version, changelog, download_url)
            update_dlg.exec()
            
    update_checker.check_finished.connect(on_update_checked)
    update_checker.start()
    app.update_checker = update_checker
    
    try:
        # Run standard Qt event loop
        sys.exit(app.exec())
    finally:
        # Make sure hook threads exit cleanly when application closes
        listener.stop()
        mouse_listener.stop()

if __name__ == "__main__":
    main()
