# app/themes.py
import os
import json
import re

THEME_SETTINGS_STYLE = {
    "dark": """
        CardFrame { background-color: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 4px; }
        QWidget#Sidebar { background-color: #161616; border-right: 1px solid rgba(255,255,255,0.08); }
        SectionLabel { color: #FFFFFF; font-size: 15px; font-weight: bold; margin-bottom: 4px; margin-top: 10px; }
        DescLabel { color: #888888; font-size: 11px; margin-bottom: 4px; }

        
        QTextBrowser, QMessageBox { color: #FFFFFF; }
        #MainContainer, #MainContainer QWidget { color: #FFFFFF; }
        QDialog#SettingsWindow, QDialog#UpdateDialog, QDialog#ThemeCreatorDialog {
            background-color: #1F1F1F;
        }
        #MainContainer {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #FFFFFF;
            background-color: #1F1F1F;
            border-radius: 12px;
        }
        QLabel#LogoLabel {
            font-size: 15px;
            font-weight: bold;
            color: #0078D4;
            padding: 4px 8px 16px 8px;
        }
        QLabel#VersionLabel {
            color: #555555;
            font-size: 11px;
        }
        QLabel#DialogTitle {
            font-size: 16px;
            font-weight: bold;
        }
        QLabel#DialogMeta, QLabel#StatusLabel {
            font-size: 13px;
            color: #888888;
        }
        QLabel#DialogSectionTitle {
            font-weight: bold;
        }
        QWidget#BottomBar {
            background-color: #1A1A1A;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        QTextBrowser#ChangelogBrowser {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            background-color: #1A1A1A;
        }
        QProgressBar#DialogProgress {
            border: 1px solid #3D3D3D;
            border-radius: 6px;
            background-color: #1A1A1A;
            text-align: center;
            color: #FFFFFF;
        }
        QProgressBar#DialogProgress::chunk {
            background-color: #0078D4;
            border-radius: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #2D2D2D;
            background-color: #1F1F1F;
            border-radius: 8px;
            top: -1px;
        }
        SidebarButton, QPushButton[navButton="true"] {
            background-color: #2D2D2D;
            border: 1px solid #3D3D3D;
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #AAAAAA;
        }
        SidebarButton:hover, QPushButton[navButton="true"]:hover {
            background-color: #353535;
            color: #FFFFFF;
        }
        SidebarButton:checked, QPushButton[navButton="true"]:checked {
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
        QPushButton[role="primary"] {
            background-color: #0078D4;
            border-color: #0078D4;
            color: #FFFFFF;
            font-weight: bold;
            padding: 7px 18px;
            border-radius: 6px;
        }
        QPushButton[role="primary"]:hover {
            background-color: #1883D7;
            border-color: #1883D7;
        }
        QPushButton[role="success"] {
            background-color: #10B981;
            border-color: #10B981;
            color: #FFFFFF;
            font-weight: bold;
        }
        QPushButton[role="success"]:hover {
            background-color: #22C55E;
            border-color: #22C55E;
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
        QListWidget#ProfileList {
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.1);
            background-color: rgba(255,255,255,0.02);
        }
        QListWidget#ProfileList::item:selected {
            background: rgba(0,120,212,0.35);
            border-radius: 4px;
        }
    """,
    
    "light": """
        CardFrame { background-color: rgba(0,0,0,0.03); border: 1px solid rgba(0,0,0,0.08); border-radius: 10px; padding: 4px; }
        QWidget#Sidebar { background-color: #F8F8F8; border-right: 1px solid rgba(0,0,0,0.08); }
        SectionLabel { color: #1C1C1C; font-size: 15px; font-weight: bold; margin-bottom: 4px; margin-top: 10px; }
        DescLabel { color: #666666; font-size: 11px; margin-bottom: 4px; }

        
        QTextBrowser, QMessageBox { color: #1C1C1C; }
        #MainContainer, #MainContainer QWidget { color: #1C1C1C; }
        QDialog#SettingsWindow, QDialog#UpdateDialog, QDialog#ThemeCreatorDialog {
            background-color: #F3F3F3;
        }
        #MainContainer {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #1C1C1C;
            background-color: #F3F3F3;
            border-radius: 12px;
        }
        QLabel#LogoLabel {
            font-size: 15px;
            font-weight: bold;
            color: #0078D4;
            padding: 4px 8px 16px 8px;
        }
        QLabel#VersionLabel {
            color: #777777;
            font-size: 11px;
        }
        QLabel#DialogTitle {
            font-size: 16px;
            font-weight: bold;
        }
        QLabel#DialogMeta, QLabel#StatusLabel {
            font-size: 13px;
            color: #666666;
        }
        QLabel#DialogSectionTitle {
            font-weight: bold;
        }
        QWidget#BottomBar {
            background-color: #ECECEC;
            border-top: 1px solid rgba(0,0,0,0.08);
        }
        QTextBrowser#ChangelogBrowser {
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 6px;
            background-color: #FFFFFF;
        }
        QProgressBar#DialogProgress {
            border: 1px solid #D0D0D0;
            border-radius: 6px;
            background-color: #FFFFFF;
            text-align: center;
            color: #1C1C1C;
        }
        QProgressBar#DialogProgress::chunk {
            background-color: #0078D4;
            border-radius: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #E5E5E5;
            background-color: #FFFFFF;
            border-radius: 8px;
            top: -1px;
        }
        SidebarButton, QPushButton[navButton="true"] {
            background-color: #E5E5E5;
            border: 1px solid #D0D0D0;
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #555555;
        }
        SidebarButton:hover, QPushButton[navButton="true"]:hover {
            background-color: #ECECEC;
            color: #1C1C1C;
        }
        SidebarButton:checked, QPushButton[navButton="true"]:checked {
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
        QPushButton[role="primary"] {
            background-color: #0078D4;
            border-color: #0078D4;
            color: #FFFFFF;
            font-weight: bold;
            padding: 7px 18px;
            border-radius: 6px;
        }
        QPushButton[role="primary"]:hover {
            background-color: #1883D7;
            border-color: #1883D7;
        }
        QPushButton[role="success"] {
            background-color: #10B981;
            border-color: #10B981;
            color: #FFFFFF;
            font-weight: bold;
        }
        QPushButton[role="success"]:hover {
            background-color: #22C55E;
            border-color: #22C55E;
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
        QListWidget#ProfileList {
            border-radius: 6px;
            border: 1px solid rgba(0,0,0,0.1);
            background-color: #FFFFFF;
        }
        QListWidget#ProfileList::item:selected {
            background: rgba(0,120,212,0.18);
            border-radius: 4px;
        }
    """,
    
    "glass": """
        CardFrame { background-color: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; padding: 4px; }
        QWidget#Sidebar { background-color: #111111; border-right: 1px solid rgba(255,255,255,0.1); }
        SectionLabel { color: #FFFFFF; font-size: 15px; font-weight: bold; margin-bottom: 4px; margin-top: 10px; }
        DescLabel { color: #AAAAAA; font-size: 11px; margin-bottom: 4px; }

        
        QTextBrowser, QMessageBox { color: #FFFFFF; }
        #MainContainer, #MainContainer QWidget { color: #FFFFFF; }
        QDialog#SettingsWindow, QDialog#UpdateDialog, QDialog#ThemeCreatorDialog {
            background-color: #1F1F1F;
        }
        #MainContainer {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #FFFFFF;
            background-color: #1F1F1F;
            border-radius: 12px;
        }
        QLabel#LogoLabel {
            font-size: 15px;
            font-weight: bold;
            color: #8FD8FF;
            padding: 4px 8px 16px 8px;
        }
        QLabel#VersionLabel {
            color: #8A8A8A;
            font-size: 11px;
        }
        QLabel#DialogTitle {
            font-size: 16px;
            font-weight: bold;
        }
        QLabel#DialogMeta, QLabel#StatusLabel {
            font-size: 13px;
            color: #AAAAAA;
        }
        QLabel#DialogSectionTitle {
            font-weight: bold;
        }
        QWidget#BottomBar {
            background-color: rgba(17, 17, 17, 180);
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        QTextBrowser#ChangelogBrowser {
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 6px;
            background-color: rgba(255,255,255,0.04);
        }
        QProgressBar#DialogProgress {
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 6px;
            background-color: rgba(255,255,255,0.06);
            text-align: center;
            color: #FFFFFF;
        }
        QProgressBar#DialogProgress::chunk {
            background-color: #0078D4;
            border-radius: 5px;
        }
        QTabWidget::pane {
            border: 1px solid rgba(255, 255, 255, 40);
            background-color: rgba(45, 45, 45, 120);
            border-radius: 10px;
            top: -1px;
        }
        SidebarButton, QPushButton[navButton="true"] {
            background-color: rgba(45, 45, 45, 100);
            border: 1px solid rgba(255, 255, 255, 30);
            border-bottom-color: transparent;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #DDDDDD;
        }
        SidebarButton:hover, QPushButton[navButton="true"]:hover {
            background-color: rgba(255, 255, 255, 40);
            color: #FFFFFF;
        }
        SidebarButton:checked, QPushButton[navButton="true"]:checked {
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
        QPushButton[role="primary"] {
            background-color: #0078D4;
            border-color: #0078D4;
            color: #FFFFFF;
            font-weight: bold;
            padding: 7px 18px;
            border-radius: 6px;
        }
        QPushButton[role="primary"]:hover {
            background-color: #1883D7;
            border-color: #1883D7;
        }
        QPushButton[role="success"] {
            background-color: #10B981;
            border-color: #10B981;
            color: #FFFFFF;
            font-weight: bold;
        }
        QPushButton[role="success"]:hover {
            background-color: #22C55E;
            border-color: #22C55E;
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
        QListWidget#ProfileList {
            border-radius: 6px;
            border: 1px solid rgba(255,255,255,0.1);
            background-color: rgba(255,255,255,0.04);
        }
        QListWidget#ProfileList::item:selected {
            background: rgba(0,120,212,0.28);
            border-radius: 4px;
        }
    """,
    
    "neon": """
        CardFrame { background-color: rgba(0,240,255,0.05); border: 1px solid rgba(0,240,255,0.2); border-radius: 10px; padding: 4px; }
        QWidget#Sidebar { background-color: #0A0A10; border-right: 1px solid rgba(0,240,255,0.3); }
        SectionLabel { color: #00F0FF; font-size: 15px; font-weight: bold; margin-bottom: 4px; margin-top: 10px; }
        DescLabel { color: #00A0A0; font-size: 11px; margin-bottom: 4px; }

        
        #MainContainer, #MainContainer QWidget {
            font-family: "Segoe UI", sans-serif;
            font-size: 13px;
            color: #E0F7FC;
        }
        QDialog#SettingsWindow, QDialog#UpdateDialog, QDialog#ThemeCreatorDialog {
            background-color: #091122;
        }
        QLabel#LogoLabel {
            font-size: 15px;
            font-weight: bold;
            color: #00F0FF;
            padding: 4px 8px 16px 8px;
        }
        QLabel#VersionLabel {
            color: #3B8BA0;
            font-size: 11px;
        }
        QLabel#DialogTitle {
            font-size: 16px;
            font-weight: bold;
        }
        QLabel#DialogMeta, QLabel#StatusLabel {
            font-size: 13px;
            color: #00AAFF;
        }
        QLabel#DialogSectionTitle {
            font-weight: bold;
        }
        QWidget#BottomBar {
            background-color: #08101C;
            border-top: 1px solid rgba(0,240,255,0.2);
        }
        QTextBrowser#ChangelogBrowser {
            border: 1px solid rgba(0,240,255,0.25);
            border-radius: 6px;
            background-color: #08101C;
        }
        QProgressBar#DialogProgress {
            border: 1px solid #004455;
            border-radius: 6px;
            background-color: #08101C;
            text-align: center;
            color: #00F0FF;
        }
        QProgressBar#DialogProgress::chunk {
            background-color: #00AEEF;
            border-radius: 5px;
        }
        QTabWidget::pane {
            border: 1px solid #00F0FF;
            background-color: #091122;
            border-radius: 8px;
            top: -1px;
        }
        SidebarButton, QPushButton[navButton="true"] {
            background-color: #091122;
            border: 1px solid #004455;
            border-bottom-color: transparent;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            padding: 8px 16px;
            margin-right: 4px;
            color: #00AAFF;
        }
        SidebarButton:hover, QPushButton[navButton="true"]:hover {
            background-color: #112244;
            color: #00F0FF;
        }
        SidebarButton:checked, QPushButton[navButton="true"]:checked {
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
        QPushButton[role="primary"] {
            background-color: #00AEEF;
            border-color: #00F0FF;
            color: #041018;
            font-weight: bold;
            padding: 7px 18px;
            border-radius: 6px;
        }
        QPushButton[role="primary"]:hover {
            background-color: #33D7FF;
            border-color: #33D7FF;
        }
        QPushButton[role="success"] {
            background-color: #0FBF9F;
            border-color: #00F0FF;
            color: #041018;
            font-weight: bold;
        }
        QPushButton[role="success"]:hover {
            background-color: #24D9B7;
            border-color: #24D9B7;
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
        QListWidget#ProfileList {
            border-radius: 6px;
            border: 1px solid rgba(0,240,255,0.2);
            background-color: #08101C;
        }
        QListWidget#ProfileList::item:selected {
            background: rgba(0,240,255,0.2);
            border-radius: 4px;
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

def _hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def get_contrast_text(hex_color):
    """Returns black or white depending on the perceived brightness of a hex color."""
    try:
        r, g, b = _hex_to_rgb(hex_color)
        luminance = (0.299 * r) + (0.587 * g) + (0.114 * b)
        return "#041018" if luminance >= 160 else "#FFFFFF"
    except Exception:
        return "#FFFFFF"

def get_settings_theme_palette(theme_name):
    """Returns theme colors used by runtime-painted UI assets such as icons."""
    theme_lower = theme_name.lower()
    if theme_lower == "dark":
        return {
            "text": "#FFFFFF",
            "muted": "#AAAAAA",
            "accent": "#0078D4",
            "on_accent": "#FFFFFF",
            "success": "#10B981",
            "on_success": "#FFFFFF",
        }
    if theme_lower == "light":
        return {
            "text": "#1C1C1C",
            "muted": "#555555",
            "accent": "#0078D4",
            "on_accent": "#FFFFFF",
            "success": "#10B981",
            "on_success": "#FFFFFF",
        }
    if theme_lower == "glass":
        return {
            "text": "#FFFFFF",
            "muted": "#DDDDDD",
            "accent": "#0078D4",
            "on_accent": "#FFFFFF",
            "success": "#10B981",
            "on_success": "#FFFFFF",
        }
    if theme_lower == "neon":
        return {
            "text": "#00F0FF",
            "muted": "#00AAFF",
            "accent": "#00AEEF",
            "on_accent": "#041018",
            "success": "#0FBF9F",
            "on_success": "#041018",
        }
    if theme_lower in CUSTOM_THEMES:
        theme_data = CUSTOM_THEMES[theme_lower].get("settings_window", {})
        text = theme_data.get("text", "#FFFFFF")
        accent = theme_data.get("accent", "#0078D4")
        success = "#10B981"
        return {
            "text": text,
            "muted": adjust_brightness(text, -0.3),
            "accent": accent,
            "on_accent": get_contrast_text(accent),
            "success": success,
            "on_success": get_contrast_text(success),
        }
    return get_settings_theme_palette("dark")

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
    QDialog#SettingsWindow, QDialog#UpdateDialog, QDialog#ThemeCreatorDialog {{
        background-color: {background};
    }}
    #MainContainer, #MainContainer QWidget {{
        font-family: "Segoe UI", sans-serif;
        font-size: 13px;
        color: {text};
    }}
    #MainContainer {{
        border-radius: 12px;
    }}
    QLabel#LogoLabel {{
        font-size: 15px;
        font-weight: bold;
        color: {accent};
        padding: 4px 8px 16px 8px;
    }}
    QLabel#VersionLabel {{
        color: {text_dimmed};
        font-size: 11px;
    }}
    QLabel#DialogTitle {{
        font-size: 16px;
        font-weight: bold;
    }}
    QLabel#DialogMeta, QLabel#StatusLabel {{
        font-size: 13px;
        color: {text_dimmed};
    }}
    QLabel#DialogSectionTitle {{
        font-weight: bold;
    }}
    QWidget#BottomBar {{
        background-color: {card_bg};
        border-top: 1px solid {border};
    }}
    QTextBrowser, QMessageBox {{
        color: {text};
    }}
    QTextBrowser#ChangelogBrowser {{
        border: 1px solid {border};
        border-radius: 6px;
        background-color: {card_bg};
    }}
    QProgressBar#DialogProgress {{
        border: 1px solid {border};
        border-radius: 6px;
        background-color: {card_bg};
        text-align: center;
        color: {text};
    }}
    QProgressBar#DialogProgress::chunk {{
        background-color: {accent};
        border-radius: 5px;
    }}
    CardFrame {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-radius: 10px;
        padding: 4px;
    }}
    SectionLabel {{
        color: {text};
        font-size: 15px;
        font-weight: bold;
        margin-bottom: 4px;
        margin-top: 10px;
    }}
    DescLabel {{
        color: {text_dimmed};
        font-size: 11px;
        margin-bottom: 4px;
    }}
    QTabWidget::pane {{
        border: 1px solid {border};
        background-color: {background};
        border-radius: 8px;
        top: -1px;
    }}
    SidebarButton, QPushButton[navButton="true"] {{
        background-color: {card_bg};
        border: 1px solid {border};
        border-bottom-color: transparent;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        padding: 8px 16px;
        margin-right: 4px;
        color: {text_dimmed};
    }}
    SidebarButton:hover, QPushButton[navButton="true"]:hover {{
        background-color: {card_bg_hover};
        color: {text};
    }}
    SidebarButton:checked, QPushButton[navButton="true"]:checked {{
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
    QPushButton[role="primary"] {{
        background-color: {accent};
        border-color: {accent};
        color: #FFFFFF;
        font-weight: bold;
        padding: 7px 18px;
        border-radius: 6px;
    }}
    QPushButton[role="primary"]:hover {{
        background-color: {accent_hover};
        border-color: {accent_hover};
    }}
    QPushButton[role="success"] {{
        background-color: #10B981;
        border-color: #10B981;
        color: #FFFFFF;
        font-weight: bold;
    }}
    QPushButton[role="success"]:hover {{
        background-color: #22C55E;
        border-color: #22C55E;
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
    QListWidget#ProfileList {{
        border-radius: 6px;
        border: 1px solid {border};
        background-color: {card_bg};
    }}
    QListWidget#ProfileList::item:selected {{
        background: rgba(0,120,212,0.35);
        border-radius: 4px;
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
