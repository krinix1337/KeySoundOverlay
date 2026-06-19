# app/themes.py

THEME_SETTINGS_STYLE = {
    "dark": """
        QMainWindow, QDialog {
            background-color: #1F1F1F;
            color: #FFFFFF;
        }
        QWidget {
            font-family: "Segoe UI", "Segoe UI Variable Text", sans-serif;
            font-size: 13px;
            color: #FFFFFF;
        }
        QTabWidget::pane {
            border: 1px solid #2D2D2D;
            background-color: #1F1F1F;
            border-radius: 8px;
            top: -1px;
        }
        QTabBar::tab {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-bottom-color: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #AAAAAA;
        }
        QTabBar::tab:hover {
            background-color: #353535;
            color: #FFFFFF;
        }
        QTabBar::tab:selected {
            background-color: #1F1F1F;
            border-color: #2D2D2D;
            color: #FFFFFF;
            border-bottom: 2px solid #0078D4;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #2D2D2D;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }
        QPushButton {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-radius: 4px;
            padding: 6px 12px;
            min-height: 20px;
            color: #FFFFFF;
        }
        QPushButton:hover {
            background-color: #3D3D3D;
            border-color: #4D4D4D;
        }
        QPushButton:pressed {
            background-color: #252525;
        }
        QPushButton:disabled {
            background-color: #1A1A1A;
            color: #666666;
            border-color: #252525;
        }
        QSlider::groove:horizontal {
            height: 4px;
            background: #444444;
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            background: #0078D4;
            width: 14px;
            margin-top: -5px;
            margin-bottom: -5px;
            border-radius: 7px;
        }
        QSlider::handle:horizontal:hover {
            background: #1883D7;
        }
        QComboBox {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-radius: 4px;
            padding: 5px;
            min-width: 120px;
            color: #FFFFFF;
        }
        QComboBox:hover {
            background-color: #353535;
        }
        QComboBox QAbstractItemView {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            selection-background-color: #0078D4;
            selection-color: #FFFFFF;
        }
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #3D3D3D;
            border-radius: 3px;
            background-color: #2D2D2D;
        }
        QCheckBox::indicator:hover {
            border-color: #0078D4;
        }
        QCheckBox::indicator:checked {
            background-color: #0078D4;
            border-color: #0078D4;
            image: url(check.png); /* Native fallback when no image */
        }
        QLabel {
            color: #E2E2E2;
        }
        QLineEdit {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-radius: 4px;
            padding: 4px;
            color: #FFFFFF;
        }
        QLineEdit:focus {
            border: 1px solid #0078D4;
        }
    """,
    
    "light": """
        QMainWindow, QDialog {
            background-color: #F3F3F3;
            color: #1C1C1C;
        }
        QWidget {
            font-family: "Segoe UI", "Segoe UI Variable Text", sans-serif;
            font-size: 13px;
            color: #1C1C1C;
        }
        QTabWidget::pane {
            border: 1px solid #E5E5E5;
            background-color: #FFFFFF;
            border-radius: 8px;
            top: -1px;
        }
        QTabBar::tab {
            background-color: #E5E5E5;
            border: 1px solid #D0D0D0;
            border-bottom-color: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #555555;
        }
        QTabBar::tab:hover {
            background-color: #ECECEC;
            color: #1C1C1C;
        }
        QTabBar::tab:selected {
            background-color: #FFFFFF;
            border-color: #E5E5E5;
            color: #1C1C1C;
            border-bottom: 2px solid #0078D4;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 16px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }
        QPushButton {
            background-color: #FFFFFF;
            border: 1px solid #D0D0D0;
            border-radius: 4px;
            padding: 6px 12px;
            min-height: 20px;
            color: #1C1C1C;
        }
        QPushButton:hover {
            background-color: #F6F6F6;
            border-color: #B0B0B0;
        }
        QPushButton:pressed {
            background-color: #ECECEC;
        }
        QPushButton:disabled {
            background-color: #E0E0E0;
            color: #999999;
            border-color: #D0D0D0;
        }
        QSlider::groove:horizontal {
            height: 4px;
            background: #CCCCCC;
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            background: #0078D4;
            width: 14px;
            margin-top: -5px;
            margin-bottom: -5px;
            border-radius: 7px;
        }
        QSlider::handle:horizontal:hover {
            background: #1883D7;
        }
        QComboBox {
            background-color: #FFFFFF;
            border: 1px solid #D0D0D0;
            border-radius: 4px;
            padding: 5px;
            min-width: 120px;
            color: #1C1C1C;
        }
        QComboBox:hover {
            background-color: #F6F6F6;
        }
        QComboBox QAbstractItemView {
            background-color: #FFFFFF;
            border: 1px solid #D0D0D0;
            selection-background-color: #0078D4;
            selection-color: #FFFFFF;
        }
        QCheckBox {
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #D0D0D0;
            border-radius: 3px;
            background-color: #FFFFFF;
        }
        QCheckBox::indicator:hover {
            border-color: #0078D4;
        }
        QCheckBox::indicator:checked {
            background-color: #0078D4;
            border-color: #0078D4;
        }
        QLabel {
            color: #2C2C2C;
        }
        QLineEdit {
            background-color: #FFFFFF;
            border: 1px solid #D0D0D0;
            border-radius: 4px;
            padding: 4px;
            color: #1C1C1C;
        }
        QLineEdit:focus {
            border: 1px solid #0078D4;
        }
    """,
    
    "glass": """
        QMainWindow, QDialog {
            background-color: rgba(28, 28, 28, 210);
            color: #FFFFFF;
        }
        QWidget {
            font-family: "Segoe UI", "Segoe UI Variable Text", sans-serif;
            font-size: 13px;
            color: #FFFFFF;
        }
        QTabWidget::pane {
            border: 1px solid rgba(255, 255, 255, 40);
            background-color: rgba(45, 45, 45, 120);
            border-radius: 10px;
            top: -1px;
        }
        QTabBar::tab {
            background-color: rgba(45, 45, 45, 100);
            border: 1px solid rgba(255, 255, 255, 30);
            border-bottom-color: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #DDDDDD;
        }
        QTabBar::tab:hover {
            background-color: rgba(255, 255, 255, 40);
            color: #FFFFFF;
        }
        QTabBar::tab:selected {
            background-color: rgba(45, 45, 45, 180);
            border-color: rgba(255, 255, 255, 50);
            color: #FFFFFF;
            border-bottom: 2px solid #0078D4;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 16px;
            background-color: rgba(255, 255, 255, 5);
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }
        QPushButton {
            background-color: rgba(255, 255, 255, 15);
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 6px;
            padding: 6px 12px;
            min-height: 20px;
            color: #FFFFFF;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 25);
            border-color: rgba(255, 255, 255, 50);
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 10);
        }
        QPushButton:disabled {
            background-color: rgba(255, 255, 255, 5);
            color: #777777;
            border-color: rgba(255, 255, 255, 10);
        }
        QSlider::groove:horizontal {
            height: 4px;
            background: rgba(255, 255, 255, 40);
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            background: #0078D4;
            width: 14px;
            margin-top: -5px;
            margin-bottom: -5px;
            border-radius: 7px;
        }
        QComboBox {
            background-color: rgba(255, 255, 255, 15);
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 6px;
            padding: 5px;
            min-width: 120px;
            color: #FFFFFF;
        }
        QComboBox:hover {
            background-color: rgba(255, 255, 255, 25);
        }
        QComboBox QAbstractItemView {
            background-color: rgba(45, 45, 45, 230);
            border: 1px solid rgba(255, 255, 255, 30);
            selection-background-color: #0078D4;
            selection-color: #FFFFFF;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid rgba(255, 255, 255, 40);
            border-radius: 4px;
            background-color: rgba(255, 255, 255, 10);
        }
        QCheckBox::indicator:hover {
            border-color: #0078D4;
        }
        QCheckBox::indicator:checked {
            background-color: #0078D4;
            border-color: #0078D4;
        }
        QLineEdit {
            background-color: rgba(255, 255, 255, 10);
            border: 1px solid rgba(255, 255, 255, 30);
            border-radius: 4px;
            padding: 4px;
            color: #FFFFFF;
        }
        QLineEdit:focus {
            border: 1px solid #0078D4;
        }
    """,
    
    "neon": """
        QMainWindow, QDialog {
            background-color: #050811;
            color: #E0F7FC;
        }
        QWidget {
            font-family: "Segoe UI", "Segoe UI Variable Text", sans-serif;
            font-size: 13px;
            color: #E0F7FC;
        }
        QTabWidget::pane {
            border: 1px solid #00F0FF;
            background-color: #091122;
            border-radius: 8px;
            top: -1px;
        }
        QTabBar::tab {
            background-color: #091122;
            border: 1px solid #004455;
            border-bottom-color: none;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #00AAFF;
        }
        QTabBar::tab:hover {
            background-color: #112244;
            color: #00F0FF;
        }
        QTabBar::tab:selected {
            background-color: #091122;
            border-color: #00F0FF;
            color: #00F0FF;
            border-bottom: 2px solid #00F0FF;
        }
        QGroupBox {
            font-weight: bold;
            border: 1px solid #004455;
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 16px;
            color: #00F0FF;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 10px;
            padding: 0 4px;
        }
        QPushButton {
            background-color: #0B1528;
            border: 1px solid #00F0FF;
            border-radius: 4px;
            padding: 6px 12px;
            min-height: 20px;
            color: #00F0FF;
        }
        QPushButton:hover {
            background-color: #0D2644;
            border-color: #00F0FF;
        }
        QPushButton:pressed {
            background-color: #070D18;
        }
        QPushButton:disabled {
            background-color: #03060C;
            color: #004455;
            border-color: #002233;
        }
        QSlider::groove:horizontal {
            height: 4px;
            background: #002233;
            border-radius: 2px;
        }
        QSlider::handle:horizontal {
            background: #00F0FF;
            width: 14px;
            margin-top: -5px;
            margin-bottom: -5px;
            border-radius: 7px;
        }
        QComboBox {
            background-color: #0B1528;
            border: 1px solid #004455;
            border-radius: 4px;
            padding: 5px;
            min-width: 120px;
            color: #00F0FF;
        }
        QComboBox:hover {
            border-color: #00F0FF;
        }
        QComboBox QAbstractItemView {
            background-color: #0B1528;
            border: 1px solid #00F0FF;
            selection-background-color: #004455;
            selection-color: #00F0FF;
        }
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid #004455;
            border-radius: 3px;
            background-color: #0B1528;
        }
        QCheckBox::indicator:hover {
            border-color: #00F0FF;
        }
        QCheckBox::indicator:checked {
            background-color: #00F0FF;
            border-color: #00F0FF;
        }
        QLineEdit {
            background-color: #0B1528;
            border: 1px solid #004455;
            border-radius: 4px;
            padding: 4px;
            color: #00F0FF;
        }
        QLineEdit:focus {
            border: 1px solid #00F0FF;
        }
    """
}

def get_theme_qss(theme_name):
    """Returns settings window QSS by theme name."""
    return THEME_SETTINGS_STYLE.get(theme_name.lower(), THEME_SETTINGS_STYLE["dark"])

def get_overlay_key_qss(theme_name, highlight_color, is_pressed=False, opacity=1.0):
    """Returns stylesheet for standard or highlighted keycap widget with adjustable opacity."""
    theme = theme_name.lower()
    
    # Active State Styling: Always fully bright and opaque
    if is_pressed:
        if theme == "neon":
            return f"""
                background-color: #00F0FF;
                border: 2px solid #FFFFFF;
                border-radius: 6px;
                color: #050811;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
        elif theme == "glass":
            return f"""
                background-color: {highlight_color};
                border: 1px solid rgba(255, 255, 255, 200);
                border-radius: 6px;
                color: #FFFFFF;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
        else: # dark, light
            return f"""
                background-color: {highlight_color};
                border: 1px solid #FFFFFF;
                border-radius: 5px;
                color: #FFFFFF;
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
            
    # Idle State Styling: Applies opacity to background and border, but keeps text solid
    else:
        # Scale background alpha channels
        bg_alpha = int(opacity * 255)
        border_alpha = int(opacity * 255)
        
        if theme == "light":
            return f"""
                background-color: rgba(255, 255, 255, {bg_alpha});
                border: 1px solid rgba(210, 210, 210, {border_alpha});
                border-radius: 5px;
                color: rgba(28, 28, 28, 255);
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
        elif theme == "glass":
            glass_bg = int(opacity * 130)
            glass_border = int(opacity * 30)
            return f"""
                background-color: rgba(45, 45, 45, {glass_bg});
                border: 1px solid rgba(255, 255, 255, {glass_border});
                border-radius: 6px;
                color: rgba(255, 255, 255, 255);
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
        elif theme == "neon":
            neon_bg = int(opacity * 40)
            neon_border = int(opacity * 120)
            return f"""
                background-color: rgba(11, 21, 40, {neon_bg});
                border: 1px solid rgba(0, 85, 100, {neon_border});
                border-radius: 6px;
                color: rgba(0, 170, 255, 255);
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
        else: # dark (default)
            return f"""
                background-color: rgba(45, 45, 45, {bg_alpha});
                border: 1px solid rgba(62, 62, 62, {border_alpha});
                border-radius: 5px;
                color: rgba(226, 226, 226, 255);
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
