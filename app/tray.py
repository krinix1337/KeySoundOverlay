# app/tray.py
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QObject
from app.utils import get_app_icon

class SystemTrayController(QObject):
    def __init__(self, app, config, settings_window, overlay_window):
        super().__init__()
        self.app = app
        self.config = config
        self.settings_window = settings_window
        self.overlay_window = overlay_window
        
        # System Tray Icon initialization
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(get_app_icon())
        self.tray_icon.setToolTip("KeySound Overlay")
        
        # Build Context Menu
        self.menu = QMenu()
        
        self.act_settings = QAction("Настройки...", self)
        self.act_settings.triggered.connect(self.show_settings)
        
        self.act_toggle_overlay = QAction("Отображать overlay", self)
        self.act_toggle_overlay.setCheckable(True)
        self.act_toggle_overlay.triggered.connect(self.toggle_overlay)
        
        self.act_toggle_sound = QAction("Включить звук", self)
        self.act_toggle_sound.setCheckable(True)
        self.act_toggle_sound.triggered.connect(self.toggle_sound)
        
        self.act_exit = QAction("Выход", self)
        self.act_exit.triggered.connect(self.exit_app)
        
        self.menu.addAction(self.act_settings)
        self.menu.addSeparator()
        self.menu.addAction(self.act_toggle_overlay)
        self.menu.addAction(self.act_toggle_sound)
        self.menu.addSeparator()
        self.menu.addAction(self.act_exit)
        
        self.tray_icon.setContextMenu(self.menu)
        
        # Single/Double click on tray icon opens settings window
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        # Sync initial menu check states
        self.sync_menu_states()
        
        # Connect settings changes to keep tray menu checkboxes updated
        self.settings_window.settings_changed.connect(self.sync_menu_states)

    def show(self):
        self.tray_icon.show()

    def sync_menu_states(self):
        """Synchronizes checkbox check states in the tray context menu with settings."""
        self.act_toggle_overlay.setChecked(self.config.get("overlay_enabled"))
        self.act_toggle_sound.setChecked(self.config.get("sound_enabled"))

    def show_settings(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def toggle_overlay(self, checked):
        self.config.set("overlay_enabled", checked)
        if checked:
            self.overlay_window.show()
        else:
            self.overlay_window.hide()
        self.settings_window.load_values()

    def toggle_sound(self, checked):
        self.config.set("sound_enabled", checked)
        self.settings_window.load_values()

    def exit_app(self):
        self.tray_icon.hide()
        self.app.quit()

    def on_tray_activated(self, reason):
        # Open settings window on clicking/double clicking tray icon
        if reason in (QSystemTrayIcon.Trigger, QSystemTrayIcon.DoubleClick):
            self.show_settings()
        elif reason == QSystemTrayIcon.MiddleClick:
            # Quick toggle overlay on middle click
            current_state = self.config.get("overlay_enabled")
            self.toggle_overlay(not current_state)
            self.sync_menu_states()
