def get_theme(name="dark"):
    if name == "glass":
        return """
        QWidget {
            color: #FFFFFF;
            font-family: 'Segoe UI Variable', 'Segoe UI', 'Inter', sans-serif;
        }
        QMainWindow, SettingsWindow {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a1a2e, stop:1 #16213e);
        }
        QFrame#CardFrame {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
        }
        QPushButton.SidebarButton {
            text-align: left;
            padding: 10px 16px;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: #b0b0b0;
            font-size: 14px;
            font-weight: 500;
        }
        QPushButton.SidebarButton:hover {
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
        }
        QPushButton.SidebarButton:checked {
            background: rgba(255, 255, 255, 0.15);
            color: #00a8ff;
            font-weight: 600;
        }
        QComboBox {
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 6px;
            padding: 6px 12px;
            color: #FFF;
        }
        QComboBox:hover {
            background-color: rgba(255, 255, 255, 0.15);
        }
        QComboBox::drop-down { border: none; }
        QSlider::groove:horizontal {
            border-radius: 4px;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
        }
        QSlider::handle:horizontal {
            background: #00a8ff;
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }
        QLabel#SectionLabel {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            padding-bottom: 4px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        """
    elif name == "neon":
        return """
        QWidget {
            color: #FFF;
            font-family: 'Segoe UI', sans-serif;
        }
        QMainWindow, SettingsWindow {
            background-color: #09090b;
        }
        QFrame#CardFrame {
            background-color: #121214;
            border: 1px solid #ff00ff;
            border-radius: 12px;
        }
        QPushButton.SidebarButton {
            text-align: left;
            padding: 10px 16px;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: #a1a1aa;
            font-size: 14px;
        }
        QPushButton.SidebarButton:hover {
            color: #ff00ff;
            background: rgba(255, 0, 255, 0.1);
        }
        QPushButton.SidebarButton:checked {
            background: rgba(255, 0, 255, 0.2);
            color: #ff00ff;
            font-weight: bold;
            border-left: 3px solid #ff00ff;
        }
        QComboBox {
            background-color: #121214;
            border: 1px solid #ff00ff;
            border-radius: 6px;
            padding: 6px 12px;
            color: #FFF;
        }
        QSlider::groove:horizontal {
            border-radius: 4px;
            height: 6px;
            background: #27272a;
        }
        QSlider::handle:horizontal {
            background: #ff00ff;
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }
        QLabel#SectionLabel {
            font-size: 18px;
            font-weight: bold;
            color: #ff00ff;
            padding-bottom: 4px;
        }
        """
    elif name == "light":
        return """
        QWidget {
            color: #111827;
            font-family: 'Segoe UI Variable', 'Segoe UI', 'Inter', sans-serif;
        }
        QMainWindow, SettingsWindow {
            background-color: #f3f4f6;
        }
        QFrame#CardFrame {
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
        }
        QPushButton.SidebarButton {
            text-align: left;
            padding: 10px 16px;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: #4b5563;
            font-size: 14px;
            font-weight: 500;
        }
        QPushButton.SidebarButton:hover {
            background: #e5e7eb;
            color: #111827;
        }
        QPushButton.SidebarButton:checked {
            background: #dbeafe;
            color: #2563eb;
            font-weight: 600;
        }
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            padding: 6px 12px;
            color: #111827;
        }
        QComboBox:hover { border: 1px solid #9ca3af; }
        QSlider::groove:horizontal {
            border-radius: 4px;
            height: 6px;
            background: #e5e7eb;
        }
        QSlider::handle:horizontal {
            background: #2563eb;
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }
        QLabel#SectionLabel {
            font-size: 18px;
            font-weight: bold;
            color: #111827;
            padding-bottom: 4px;
            border-bottom: 1px solid #e5e7eb;
        }
        """
    else: # Dark Theme (Modern Fluent)
        return """
        QWidget {
            color: #f3f4f6;
            font-family: 'Segoe UI Variable', 'Segoe UI', 'Inter', sans-serif;
        }
        QMainWindow, SettingsWindow {
            background-color: #111827;
        }
        QFrame#CardFrame {
            background-color: #1f2937;
            border: 1px solid #374151;
            border-radius: 12px;
        }
        QPushButton.SidebarButton {
            text-align: left;
            padding: 10px 16px;
            background: transparent;
            border: none;
            border-radius: 8px;
            color: #9ca3af;
            font-size: 14px;
            font-weight: 500;
        }
        QPushButton.SidebarButton:hover {
            background: #374151;
            color: #f3f4f6;
        }
        QPushButton.SidebarButton:checked {
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            font-weight: 600;
        }
        QComboBox {
            background-color: #374151;
            border: 1px solid #4b5563;
            border-radius: 6px;
            padding: 6px 12px;
            color: #f3f4f6;
        }
        QComboBox:hover {
            background-color: #4b5563;
        }
        QComboBox::drop-down { border: none; }
        QSlider::groove:horizontal {
            border-radius: 4px;
            height: 6px;
            background: #374151;
        }
        QSlider::handle:horizontal {
            background: #3b82f6;
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }
        QLabel#SectionLabel {
            font-size: 18px;
            font-weight: bold;
            color: #f3f4f6;
            padding-bottom: 4px;
            border-bottom: 1px solid #374151;
        }
        """
