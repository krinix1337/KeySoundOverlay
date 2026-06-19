; setup.iss
; Professional Inno Setup script for KeySound Overlay

[Setup]
AppName=KeySound Overlay
AppVersion=1.0.0
DefaultDirName={localappdata}\Programs\KeySoundOverlay
DefaultGroupName=KeySound Overlay
DisableProgramGroupPage=yes
OutputDir=dist
OutputBaseFilename=KeySoundOverlay_Setup
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
