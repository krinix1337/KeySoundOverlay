; setup.iss
; Professional Inno Setup script for KeySound Overlay

[Setup]
WizardImageFile=assets\wizard_banner.bmp
WizardSmallImageFile=assets\wizard_small.bmp
AppPublisher=KeySound Team
AppSupportURL=https://github.com/
AppUpdatesURL=https://github.com/

AppName=KeySound Overlay
AppVersion=1.4.0
DefaultDirName={localappdata}\Programs\KeySoundOverlay
DefaultGroupName=KeySound Overlay
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=KeySoundOverlay_1.4.0_Setup
SetupIconFile=assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\KeySoundOverlay.exe

[Files]
Source: "dist\KeySoundOverlay\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion

[Icons]
Name: "{group}\KeySound Overlay"; Filename: "{app}\KeySoundOverlay.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\KeySound Overlay"; Filename: "{app}\KeySoundOverlay.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\KeySoundOverlay.exe"; Description: "Запустить KeySound Overlay"; Flags: nowait postinstall skipifsilent

[Messages]
WelcomeLabel2=KeySound Overlay — это стильная программа, которая добавляет звуки механической клавиатуры при печати и отображает красивые визуальные эффекты (анимации нажатий) прямо на вашем экране. Вы можете выбрать множество свитчей и настроить темы под себя!%n%nНажмите «Далее», чтобы продолжить установку.
