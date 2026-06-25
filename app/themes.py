# app/themes.py
import os
import json
import re

THEME_SETTINGS_STYLE = {
    "dark": """
        CardFrame { background-color: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); }
        QWidget#Sidebar { background-color: #161616; border-right: 1px solid rgba(255,255,255,0.08); }
        SectionLabel { color: #FFFFFF; }
        DescLabel { color: #888888; }

        QMainWindow, QDialog {
            background-color: #1F1F1F;
            color: #FFFFFF;
        }
        QWidget, QTextBrowser, QMessageBox {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #FFFFFF;
            background-color: #1F1F1F;
        }
        QTabWidget::pane {
            border: 1px solid #2D2D2D;
            background-color: #1F1F1F;
            border-radius: 8px;
            top: -1px;
        }
        SidebarButton {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #AAAAAA;
        }
        SidebarButton:hover {
            background-color: #353535;
            color: #FFFFFF;
        }
        SidebarButton:checked {
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
             /* Native fallback when no image */
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
        CardFrame { background-color: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.08); }
        QWidget#Sidebar { background-color: #F8F8F8; border-right: 1px solid rgba(0,0,0,0.08); }
        SectionLabel { color: #1C1C1C; }
        DescLabel { color: #666666; }

        QMainWindow, QDialog {
            background-color: #F3F3F3;
            color: #1C1C1C;
        }
        QWidget, QTextBrowser, QMessageBox {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #1C1C1C;
            background-color: #F3F3F3;
        }
        QTabWidget::pane {
            border: 1px solid #E5E5E5;
            background-color: #FFFFFF;
            border-radius: 8px;
            top: -1px;
        }
        SidebarButton {
            background-color: #E5E5E5;
            border: 1px solid #D0D0D0;
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #555555;
        }
        SidebarButton:hover {
            background-color: #ECECEC;
            color: #1C1C1C;
        }
        SidebarButton:checked {
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
        CardFrame { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        QWidget#Sidebar { background-color: #111111; border-right: 1px solid rgba(255,255,255,0.1); }
        SectionLabel { color: #FFFFFF; }
        DescLabel { color: #AAAAAA; }

        QMainWindow, QDialog {
            background-color: #1C1C1C;
            color: #FFFFFF;
        }
        QWidget, QTextBrowser, QMessageBox {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #FFFFFF;
            background-color: #1F1F1F;
        }
        QTabWidget::pane {
            border: 1px solid rgba(255, 255, 255, 40);
            background-color: rgba(45, 45, 45, 120);
            border-radius: 10px;
            top: -1px;
        }
        SidebarButton {
            background-color: rgba(45, 45, 45, 100);
            border: 1px solid rgba(255, 255, 255, 30);
            border-bottom-color: transparent;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #DDDDDD;
        }
        SidebarButton:hover {
            background-color: rgba(255, 255, 255, 40);
            color: #FFFFFF;
        }
        SidebarButton:checked {
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
        CardFrame { background-color: rgba(0,240,255,0.05); border: 1px solid rgba(0,240,255,0.2); }
        QWidget#Sidebar { background-color: #0A0A10; border-right: 1px solid rgba(0,240,255,0.3); }
        SectionLabel { color: #00F0FF; }
        DescLabel { color: #00A0A0; }

        QMainWindow, QDialog {
            background-color: #050811;
            color: #E0F7FC;
        }
        QWidget {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #E0F7FC;
        }
        QTabWidget::pane {
            border: 1px solid #00F0FF;
            background-color: #091122;
            border-radius: 8px;
            top: -1px;
        }
        SidebarButton {
            background-color: #091122;
            border: 1px solid #004455;
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #00AAFF;
        }
        SidebarButton:hover {
            background-color: #112244;
            color: #00F0FF;
        }
        SidebarButton:checked {
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
    """Returns settings window QSS by theme name or loaded custom theme."""
    theme_lower = theme_name.lower()
    if theme_lower in THEME_SETTINGS_STYLE:
        return THEME_SETTINGS_STYLE[theme_lower]
    elif theme_lower in CUSTOM_THEMES:
        theme_data = CUSTOM_THEMES[theme_lower]
        # Generate dynamic QSS using custom colors
        bg = theme_data.get("settings_window", {}).get("background", "#1F1F1F")
        text = theme_data.get("settings_window", {}).get("text", "#FFFFFF")
        accent = theme_data.get("settings_window", {}).get("accent", "#0078D4")
        card_bg = theme_data.get("settings_window", {}).get("card_bg", "#2D2D2D")
        border = theme_data.get("settings_window", {}).get("border", "#3D3D3D")
        
        text_dimmed = adjust_brightness(text, -0.3)
        card_bg_hover = adjust_brightness(card_bg, 0.08)
        card_bg_pressed = adjust_brightness(card_bg, -0.05)
        border_hover = adjust_brightness(border, 0.15)
        accent_hover = adjust_brightness(accent, 0.12)
        
        return CUSTOM_SETTINGS_TEMPLATE.format(
            background=bg,
            text=text,
            accent=accent,
            card_bg=card_bg,
            border=border,
            text_dimmed=text_dimmed,
            card_bg_hover=card_bg_hover,
            card_bg_pressed=card_bg_pressed,
            border_hover=border_hover,
            accent_hover=accent_hover
        )
    return THEME_SETTINGS_STYLE["dark"]

def get_overlay_key_qss(theme_name, highlight_color, is_pressed=False, opacity=1.0):
    """Returns stylesheet for standard or highlighted keycap widget with adjustable opacity."""
    theme_lower = theme_name.lower()
    
    # Check if this is a custom theme
    if theme_lower in CUSTOM_THEMES:
        t_data = CUSTOM_THEMES[theme_lower].get("overlay", {})
        radius = t_data.get("key_radius", 5)
        
        if is_pressed:
            bg = t_data.get("key_active_bg", highlight_color)
            border = t_data.get("key_active_border", "#FFFFFF")
            text = t_data.get("key_active_text", "#FFFFFF")
            
            return f"""
                background-color: {bg};
                border: 1px solid {border};
                border-radius: {radius}px;
                color: {text};
                font-weight: bold;
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
        else:
            bg = t_data.get("key_idle_bg", "rgba(45, 45, 45, 255)")
            border = t_data.get("key_idle_border", "rgba(62, 62, 62, 255)")
            text = t_data.get("key_idle_text", "#FFFFFF")
            
            bg_rgba = parse_to_rgba(bg, opacity)
            border_rgba = parse_to_rgba(border, opacity)
            text_rgba = parse_to_rgba(text, 1.0)
            
            return f"""
                background-color: {bg_rgba};
                border: 1px solid {border_rgba};
                border-radius: {radius}px;
                color: {text_rgba};
                font-family: "Segoe UI", sans-serif;
                font-size: 11px;
            """
            
    # Fallback to predefined themes
    theme = theme_lower
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
    else:
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

# CUSTOM THEMES DATA & REGISTRY
CUSTOM_THEMES = {}

def register_custom_theme(theme_id, theme_data):
    CUSTOM_THEMES[theme_id] = theme_data

def load_custom_themes(app_data_dir):
    themes_dir = os.path.join(app_data_dir, "themes")
    if not os.path.exists(themes_dir):
        try:
            os.makedirs(themes_dir)
        except Exception:
            pass
            
    CUSTOM_THEMES.clear()
    custom_list = []
    
    if os.path.exists(themes_dir):
        for filename in os.listdir(themes_dir):
            if filename.endswith(".json"):
                path = os.path.join(themes_dir, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    theme_id = os.path.splitext(filename)[0]
                    display_name = data.get("theme_display_name", theme_id)
                    CUSTOM_THEMES[theme_id.lower()] = data
                    custom_list.append((display_name, theme_id.lower()))
                except Exception as e:
                    print(f"Error loading custom theme {filename}: {e}")
    return custom_list

def adjust_brightness(hex_color, amount):
    """Adjusts brightness of a hex color by a specified float percent (-1.0 to 1.0)."""
    try:
        hex_color = hex_color.lstrip('#')
        rgb = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
        new_rgb = []
        for c in rgb:
            new_c = int(c + amount * 255)
            new_c = max(0, min(255, new_c))
            new_rgb.append(new_c)
        return "#{:02X}{:02X}{:02X}".format(*new_rgb)
    except Exception:
        return hex_color

def parse_to_rgba(color_str, opacity_multiplier=1.0):
    """Converts hex, rgb, or rgba string to rgba(...) with opacity multiplier applied."""
    try:
        color_str = color_str.strip()
        rgba_match = re.match(r'rgba\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+|[\d\.]+)\s*\)', color_str, re.IGNORECASE)
        if rgba_match:
            r, g, b, a = rgba_match.groups()
            a_val = float(a)
            if a_val > 1.0:
                a_val = a_val / 255.0
            new_a = int(a_val * opacity_multiplier * 255)
            return f"rgba({r}, {g}, {b}, {new_a})"
            
        rgb_match = re.match(r'rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', color_str, re.IGNORECASE)
        if rgb_match:
            r, g, b = rgb_match.groups()
            new_a = int(opacity_multiplier * 255)
            return f"rgba({r}, {g}, {b}, {new_a})"
            
        if color_str.startswith('#'):
            hex_color = color_str.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join(c*2 for c in hex_color)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            new_a = int(opacity_multiplier * 255)
            return f"rgba({r}, {g}, {b}, {new_a})"
    except Exception as e:
        print(f"Error parsing color '{color_str}': {e}")
    return color_str

# CUSTOM THEME STYLESHEET TEMPLATE
CUSTOM_SETTINGS_TEMPLATE = """
    QMainWindow, QDialog {{
        background-color: {background};
        color: {text};
    }}
    QWidget {{
        font-family: "Segoe UI", sans-serif;
        font-size: 13px;
        color: {text};
    }}
    QTabWidget::pane {{
        border: 1px solid {border};
        background-color: {background};
        border-radius: 8px;
        top: -1px;
    }}
    SidebarButton {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-bottom-color: transparent;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 8px 16px;
        margin-right: 4px;
        color: {text_dimmed};
    }}
    SidebarButton:hover {{
        background-color: {card_bg_hover};
        color: {text};
    }}
    SidebarButton:checked {{
        background-color: {background};
        border-color: {border};
        color: {text};
        border-bottom: 2px solid {accent};
    }}
    QGroupBox {{
        font-weight: bold;
        border: 1px solid {border};
        border-radius: 6px;
        margin-top: 12px;
        padding-top: 16px;
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 10px;
        padding: 0 4px;
    }}
    QPushButton {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 6px 12px;
        min-height: 20px;
        color: {text};
    }}
    QPushButton:hover {{
        background-color: {card_bg_hover};
        border-color: {border_hover};
    }}
    QPushButton:pressed {{
        background-color: {card_bg_pressed};
    }}
    QPushButton:disabled {{
        background-color: {background};
        color: {text_dimmed};
        border-color: {border};
    }}
    QSlider::groove:horizontal {{
        height: 4px;
        background: {border};
        border-radius: 2px;
    }}
    QSlider::handle:horizontal {{
        background: {accent};
        width: 14px;
        margin-top: -5px;
        margin-bottom: -5px;
        border-radius: 7px;
    }}
    QSlider::handle:horizontal:hover {{
        background: {accent_hover};
    }}
    QComboBox {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 5px;
        min-width: 120px;
        color: {text};
    }}
    QComboBox:hover {{
        background-color: {card_bg_hover};
    }}
    QComboBox QAbstractItemView {{
        background-color: {card_bg};
        border: 1px solid {border};
        selection-background-color: {accent};
        selection-color: {text};
        color: {text};
    }}
    QLineEdit {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 4px;
        padding: 4px;
        color: {text};
    }}
    QLineEdit:focus {{
        border: 1px solid {accent};
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {border};
        border-radius: 3px;
        background-color: {card_bg};
    }}
    QCheckBox::indicator:hover {{
        border-color: {accent};
    }}
    QCheckBox::indicator:checked {{
        background-color: {accent};
        border-color: {accent};
    }}
"""
