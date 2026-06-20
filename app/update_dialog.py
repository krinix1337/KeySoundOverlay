# app/update_dialog.py
import os
import sys
import tempfile
import subprocess
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextBrowser, 
    QPushButton, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
from app.update_manager import UpdateCheckerWorker, FileDownloaderWorker, CURRENT_VERSION
from app.themes import get_theme_qss
from app.utils import get_app_icon

class UpdateDialog(QDialog):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.download_url = ""
        self.latest_version = ""
        self.downloader = None
        self.temp_installer_path = ""
        
        self.setWindowTitle("Доступно обновление!")
        self.setWindowIcon(get_app_icon())
        self.resize(450, 350)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowCloseButtonHint)
        self.setStyleSheet(get_theme_qss(self.config.get("theme")))
        
        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header Label
        self.lbl_title = QLabel("Доступна новая версия приложения!")
        self.lbl_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.layout.addWidget(self.lbl_title)
        
        # Versions info
        self.lbl_version = QLabel()
        self.lbl_version.setStyleSheet("font-size: 13px; color: #888888;")
        self.layout.addWidget(self.lbl_version)
        
        # Changelog browser
        self.lbl_changelog_title = QLabel("Список изменений:")
        self.lbl_changelog_title.setStyleSheet("font-weight: bold;")
        self.layout.addWidget(self.lbl_changelog_title)
        
        self.txt_changelog = QTextBrowser()
        self.txt_changelog.setOpenExternalLinks(True)
        self.txt_changelog.setStyleSheet("border: 1px solid rgba(255,255,255,20); border-radius: 6px;")
        self.layout.addWidget(self.txt_changelog)
        
        # Progress Bar (Hidden by default)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)
        
        self.lbl_status = QLabel("Скачивание...")
        self.lbl_status.setVisible(False)
        self.layout.addWidget(self.lbl_status)
        
        # Buttons Layout
        self.btn_layout = QHBoxLayout()
        self.btn_later = QPushButton("Позже")
        self.btn_later.clicked.connect(self.reject)
        
        self.btn_update = QPushButton("Обновить сейчас")
        self.btn_update.clicked.connect(self.start_download)
        self.btn_update.setDefault(True)
        
        self.btn_layout.addStretch()
        self.btn_layout.addWidget(self.btn_later)
        self.btn_layout.addWidget(self.btn_update)
        self.layout.addLayout(self.btn_layout)

    def set_update_info(self, latest_version, changelog, download_url):
        self.latest_version = latest_version
        self.download_url = download_url
        self.lbl_version.setText(f"Текущая версия: {CURRENT_VERSION} ➔ Новая версия: {latest_version}")
        self.txt_changelog.setHtml(changelog.replace("\n", "<br>"))

    def start_download(self):
        if not self.download_url:
            QMessageBox.warning(self, "Ошибка", "Не удалось найти ссылку для скачивания обновления.")
            self.reject()
            return
            
        self.btn_update.setEnabled(False)
        self.btn_later.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.lbl_status.setVisible(True)
        self.lbl_status.setText("Соединение с сервером...")
        
        # Get standard windows temporary path
        temp_dir = tempfile.gettempdir()
        self.temp_installer_path = os.path.join(temp_dir, "KeySoundOverlay_Setup.exe")
        
        # Initialize background downloader worker
        self.downloader = FileDownloaderWorker(self.download_url, self.temp_installer_path)
        self.downloader.progress.connect(self.update_progress)
        self.downloader.finished.connect(self.on_download_finished)
        self.downloader.failed.connect(self.on_download_failed)
        self.downloader.start()

    def update_progress(self, percent):
        self.progress_bar.setValue(percent)
        self.lbl_status.setText(f"Скачивание установщика: {percent}%")

    def on_download_finished(self, local_path):
        self.lbl_status.setText("Скачивание завершено! Запуск установщика...")
        QTimer.singleShot(1000, lambda: self.launch_installer(local_path))

    def on_download_failed(self, error_msg):
        self.progress_bar.setVisible(False)
        self.lbl_status.setVisible(False)
        self.btn_update.setEnabled(True)
        self.btn_later.setEnabled(True)
        QMessageBox.critical(self, "Ошибка обновления", f"Не удалось загрузить обновление:\n{error_msg}")

    def launch_installer(self, path):
        try:
            if os.path.exists(path):
                # Run the installer silently or normally (which triggers shutdown of the app)
                # Inno Setup installer will handle files overwrite.
                # It runs elevated or standard depending on setup.iss configuration.
                os.startfile(path)
                # Exit the current Python process immediately to release lockfile/sharedMemory
                # and allow the installer to replace key_sound_overlay executables.
                sys.exit(0)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить установщик:\n{str(e)}")
            self.reject()
