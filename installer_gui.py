# installer_gui.py
import sys
import os
import shutil
import winreg
from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QWidget, QLabel, QPushButton, QLineEdit, QProgressBar, QCheckBox,
    QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont

def get_resource_path(relative_path):
    """Gets absolute path to resources inside PyInstaller temp dir or local directory."""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    return os.path.join(base_path, relative_path)

def get_installer_icon():
    """Returns application QIcon. Tries to load assets/icon.ico, generates fallback if missing."""
    icon_path = get_resource_path("assets/icon.ico")
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    
    # Fallback setup icon
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor("#0078D4"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
    painter.setPen(QColor("#FFFFFF"))
    font = QFont("Segoe UI", 16, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "SETUP")
    painter.end()
    return QIcon(pixmap)

class InstallWorker(QThread):
    progress = Signal(int, str)
    finished = Signal(bool, str)

    def __init__(self, target_dir):
        super().__init__()
        self.target_dir = target_dir

    def run(self):
        try:
            dest_exe = os.path.join(self.target_dir, "KeySoundOverlay.exe")
            self.progress.emit(10, "Создание папок...")
            if not os.path.exists(self.target_dir):
                os.makedirs(self.target_dir, exist_ok=True)
            QThread.msleep(300)

            # Copy application directory contents
            self.progress.emit(30, "Копирование файлов приложения...")
            src_app_dir = get_resource_path("KeySoundOverlay")
            
            if os.path.exists(src_app_dir):
                for item in os.listdir(src_app_dir):
                    s = os.path.join(src_app_dir, item)
                    d = os.path.join(self.target_dir, item)
                    if os.path.isdir(s):
                        if os.path.exists(d):
                            shutil.rmtree(d)
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
            else:
                self.finished.emit(False, "Папка приложения KeySoundOverlay не найдена во встроенном архиве установщика!")
                return
            QThread.msleep(600)

            # Shortcuts creation (PowerShell script helper)
            self.progress.emit(70, "Создание ярлыков...")
            desktop_dir = [SystemEnvironment_GetFolderPath(0)]  # Desktop
            desktop_lnk = os.path.join(desktop_dir[0], "KeySound Overlay.lnk")
            
            startmenu_dir = [SystemEnvironment_GetFolderPath(2)]  # Start Menu / Programs
            startmenu_lnk = os.path.join(startmenu_dir[0], "KeySound Overlay.lnk")

            self.create_shortcut(dest_exe, self.target_dir, desktop_lnk)
            self.create_shortcut(dest_exe, self.target_dir, startmenu_lnk)
            QThread.msleep(200)

            # Uninstall registry keys registration
            self.progress.emit(90, "Регистрация деинсталлятора в Windows...")
            self.register_uninstaller(dest_exe)
            QThread.msleep(200)

            self.progress.emit(100, "Установка завершена!")
            self.finished.emit(True, "")

        except Exception as e:
            self.finished.emit(False, str(e))

    def create_shortcut(self, target, working_dir, shortcut_path):
        import subprocess
        try:
            # Escape backslashes for PowerShell command string
            esc_shortcut = shortcut_path.replace('"', '`"')
            esc_target = target.replace('"', '`"')
            esc_working = working_dir.replace('"', '`"')
            cmd = (
                f'$WshShell = New-Object -ComObject WScript.Shell; '
                f'$Shortcut = $WshShell.CreateShortcut("{esc_shortcut}"); '
                f'$Shortcut.TargetPath = "{esc_target}"; '
                f'$Shortcut.WorkingDirectory = "{esc_working}"; '
                f'$Shortcut.IconLocation = "{esc_target}"; '
                f'$Shortcut.Save()'
            )
            subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, check=True)
        except Exception as e:
            print(f"Error creating shortcut: {e}")

    def register_uninstaller(self, dest_exe):
        app_name = "KeySoundOverlay"
        reg_path = r"Software\Microsoft\Windows\CurrentVersion\Uninstall"
        
        # Write uninstaller script files
        uninstall_ps = os.path.join(self.target_dir, "uninstall.ps1")
        uninstall_bat = os.path.join(self.target_dir, "uninstall.bat")

        desktop_dir = [SystemEnvironment_GetFolderPath(0)]
        startmenu_dir = [SystemEnvironment_GetFolderPath(2)]

        un_ps_content = f"""$AppName = "{app_name}"
$TargetDir = "{self.target_dir}"
$ShortcutPath = Join-Path "{desktop_dir[0]}" "KeySound Overlay.lnk"
$StartMenuPath = Join-Path "{startmenu_dir[0]}" "KeySound Overlay.lnk"

Write-Host "Uninstalling KeySound Overlay..." -ForegroundColor Yellow

if (Test-Path $ShortcutPath) {{ Remove-Item $ShortcutPath -Force }}
if (Test-Path $StartMenuPath) {{ Remove-Item $StartMenuPath -Force }}

$RegRunKey = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
if (Get-ItemProperty -Path $RegRunKey -Name $AppName -ErrorAction SilentlyContinue) {{
    Remove-ItemProperty -Path $RegRunKey -Name $AppName -Force
}}

$RegUninstallKey = "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\$AppName"
if (Test-Path $RegUninstallKey) {{
    Remove-Item -Path $RegUninstallKey -Recurse -Force
}}

if (Test-Path $TargetDir) {{
    Get-ChildItem -Path $TargetDir -Exclude uninstall.ps1 | Remove-Item -Recurse -Force
    Start-Process cmd -ArgumentList "/c timeout /t 1 && rmdir /s /q `"$TargetDir`"" -WindowStyle Hidden
}}
Write-Host "Uninstall complete!" -ForegroundColor Green
"""
        with open(uninstall_ps, "w", encoding="utf-8") as f:
            f.write(un_ps_content)

        with open(uninstall_bat, "w") as f:
            f.write(f"@echo off\r\npowershell -NoProfile -ExecutionPolicy Bypass -File \"%~dp0uninstall.ps1\"\r\n")

        try:
            # Register in Windows Apps and Features Settings registry
            key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, f"{reg_path}\\{app_name}", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, "KeySound Overlay")
            winreg.SetValueEx(key, "DisplayVersion", 0, winreg.REG_SZ, "1.6.0")
            winreg.SetValueEx(key, "Publisher", 0, winreg.REG_SZ, "KeySound Dev")
            winreg.SetValueEx(key, "UninstallString", 0, winreg.REG_SZ, f'"{uninstall_bat}"')
            winreg.SetValueEx(key, "DisplayIcon", 0, winreg.REG_SZ, dest_exe)
            winreg.CloseKey(key)
        except Exception as e:
            print(f"Error registering uninstaller: {e}")

# Helper to resolve windows special folders
def SystemEnvironment_GetFolderPath(folder_id):
    import ctypes
    buf = ctypes.create_unicode_buffer(300)
    # 0 = Desktop, 2 = Programs (Start menu)
    # SHGetSpecialFolderPathW API
    ctypes.windll.shell32.SHGetSpecialFolderPathW(None, buf, folder_id, False)
    return buf.value

# UI Theme QSS
QSS_STYLE = """
    QDialog {
        background-color: #1A1A1E;
        color: #FFFFFF;
    }
    QWidget {
        font-family: "Segoe UI", sans-serif;
        font-size: 13px;
        color: #FFFFFF;
    }
    QPushButton {
        background-color: #2D2D32;
        border: 1px solid #3E3E42;
        border-radius: 5px;
        padding: 6px 14px;
        min-height: 20px;
        color: #FFFFFF;
    }
    QPushButton:hover {
        background-color: #3E3E42;
        border-color: #4E4E52;
    }
    QPushButton:pressed {
        background-color: #1E1E22;
    }
    QPushButton#BtnInstall {
        background-color: #0078D4;
        border-color: #0084E7;
    }
    QPushButton#BtnInstall:hover {
        background-color: #1883D7;
    }
    QLineEdit {
        background-color: #25252A;
        border: 1px solid #3E3E42;
        border-radius: 4px;
        padding: 5px;
        color: #FFFFFF;
    }
    QProgressBar {
        border: 1px solid #3E3E42;
        border-radius: 4px;
        background-color: #25252A;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #0078D4;
        border-radius: 3px;
    }
"""

class InstallerWizard(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Установка KeySound Overlay")
        self.setWindowIcon(get_installer_icon())
        self.resize(520, 360)
        self.setStyleSheet(QSS_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint | Qt.WindowCloseButtonHint)
        
        self.target_dir = os.path.join(os.environ.get("LOCALAPPDATA"), "Programs", "KeySoundOverlay")
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Stacked pages
        self.pages = QStackedWidget(self)
        self.layout.addWidget(self.pages)
        
        self.build_page_welcome()
        self.build_page_folder()
        self.build_page_installing()
        self.build_page_finished()
        
        # Navigation buttons layout
        self.nav_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_back = QPushButton("< Назад")
        self.btn_back.clicked.connect(self.go_back)
        self.btn_back.setEnabled(False)
        
        self.btn_next = QPushButton("Далее >")
        self.btn_next.clicked.connect(self.go_next)
        
        self.nav_layout.addWidget(self.btn_cancel)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.btn_back)
        self.nav_layout.addWidget(self.btn_next)
        self.layout.addLayout(self.nav_layout)
        
        self.current_page = 0
        self.worker = None

    def build_page_welcome(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        
        title = QLabel("Установка KeySound Overlay")
        font = QFont("Segoe UI", 18, QFont.Bold)
        title.setFont(font)
        title.setStyleSheet("color: #0078D4;")
        
        intro = QLabel(
            "Вас приветствует мастер установки KeySound Overlay!\n\n"
            "Эта программа установит KeySound Overlay — приложение для воспроизведения "
            "звуков нажатия клавиш и отображения оверлея клавиатуры поверх всех окон.\n\n"
            "Нажмите «Далее», чтобы продолжить."
        )
        intro.setWordWrap(True)
        
        layout.addWidget(title)
        layout.addWidget(intro)
        layout.addStretch()
        self.pages.addWidget(page)

    def build_page_folder(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        
        title = QLabel("Выбор папки установки")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        desc = QLabel("Программа будет установлена в следующую папку:")
        
        folder_layout = QHBoxLayout()
        self.txt_folder = QLineEdit(self.target_dir)
        btn_browse = QPushButton("Обзор...")
        btn_browse.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.txt_folder)
        folder_layout.addWidget(btn_browse)
        
        space_desc = QLabel("Требуется свободного места: ~65 МБ")
        space_desc.setStyleSheet("color: #888888; font-size: 11px;")
        
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addLayout(folder_layout)
        layout.addWidget(space_desc)
        layout.addStretch()
        self.pages.addWidget(page)

    def build_page_installing(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        
        title = QLabel("Установка приложения...")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        self.lbl_status = QLabel("Подготовка к копированию файлов...")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        layout.addWidget(title)
        layout.addWidget(self.lbl_status)
        layout.addWidget(self.progress_bar)
        layout.addStretch()
        self.pages.addWidget(page)

    def build_page_finished(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        
        title = QLabel("Завершение мастера установки")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #10B981;")
        
        desc = QLabel(
            "Приложение KeySound Overlay было успешно установлено на ваш компьютер.\n\n"
            "Ярлыки запуска добавлены на Рабочий стол и в меню Пуск.\n\n"
            "Нажмите «Готово», чтобы закрыть программу установки."
        )
        desc.setWordWrap(True)
        
        self.chk_launch = QCheckBox("Запустить KeySound Overlay сейчас")
        self.chk_launch.setChecked(True)
        
        layout.addWidget(title)
        layout.addWidget(desc)
        layout.addWidget(self.chk_launch)
        layout.addStretch()
        self.pages.addWidget(page)

    def go_back(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.pages.setCurrentIndex(self.current_page)
            self.update_nav_buttons()

    def go_next(self):
        if self.current_page == 0:
            self.current_page += 1
            self.pages.setCurrentIndex(self.current_page)
            self.update_nav_buttons()
        elif self.current_page == 1:
            # Confirm path and start install
            self.target_dir = self.txt_folder.text()
            self.current_page += 1
            self.pages.setCurrentIndex(self.current_page)
            self.update_nav_buttons()
            self.start_install()
        elif self.current_page == 3:
            # Finish installation
            if self.chk_launch.isChecked():
                self.launch_app()
            self.accept()

    def update_nav_buttons(self):
        self.btn_back.setEnabled(self.current_page in (1, 2) and self.current_page != 2) # Block back during install
        
        if self.current_page == 1:
            self.btn_next.setText("Установить")
            self.btn_next.setObjectName("BtnInstall")
            self.btn_next.setStyleSheet(QSS_STYLE) # reload stylesheet to apply ID styling
        elif self.current_page == 2:
            self.btn_next.setText("Установка...")
            self.btn_next.setEnabled(False)
            self.btn_back.setEnabled(False)
            self.btn_cancel.setEnabled(False)
        elif self.current_page == 3:
            self.btn_next.setText("Готово")
            self.btn_next.setEnabled(True)
            self.btn_back.setEnabled(False)
            self.btn_cancel.setEnabled(False)
        else:
            self.btn_next.setText("Далее >")
            self.btn_next.setEnabled(True)

    def browse_folder(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Выберите папку установки", self.target_dir)
        if dir_path:
            self.txt_folder.setText(os.path.join(dir_path, "KeySoundOverlay"))

    def start_install(self):
        self.worker = InstallWorker(self.target_dir)
        self.worker.progress.connect(self.on_install_progress)
        self.worker.finished.connect(self.on_install_finished)
        self.worker.start()

    def on_install_progress(self, val, msg):
        self.progress_bar.setValue(val)
        self.lbl_status.setText(msg)

    def on_install_finished(self, success, err_msg):
        if success:
            self.current_page = 3
            self.pages.setCurrentIndex(self.current_page)
            self.update_nav_buttons()
        else:
            QMessageBox.critical(self, "Ошибка установки", f"Произошла ошибка во время установки:\n{err_msg}")
            self.current_page = 1
            self.pages.setCurrentIndex(self.current_page)
            self.update_nav_buttons()

    def launch_app(self):
        app_exe = os.path.join(self.target_dir, "KeySoundOverlay.exe")
        if os.path.exists(app_exe):
            import subprocess
            subprocess.Popen([app_exe], cwd=self.target_dir)

def main():
    app = QApplication(sys.argv)
    wizard = InstallerWizard()
    wizard.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
