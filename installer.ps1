# installer.ps1
# Modern Windows Local App Installer for KeySound Overlay

$AppName = "KeySoundOverlay"
$TargetDir = "$env:LOCALAPPDATA\Programs\$AppName"

# Dynamically resolve Desktop and Start Menu paths using .NET special folders (handles OneDrive & localizations)
$DesktopDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$ShortcutPath = Join-Path $DesktopDir "KeySound Overlay.lnk"

$StartMenuProgramsDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Programs)
$StartMenuPath = Join-Path $StartMenuProgramsDir "KeySound Overlay.lnk"

# 1. Create target directory
if (-not (Test-Path $TargetDir)) {
    New-Item -Path $TargetDir -ItemType Directory -Force | Out-Null
}

# 2. Copy compiled application directory contents
Write-Host "Copying files to installation directory..." -ForegroundColor Cyan
if (Test-Path "dist\KeySoundOverlay") {
    if (-not (Test-Path $TargetDir)) {
        New-Item -Path $TargetDir -ItemType Directory -Force | Out-Null
    }
    # Copy all items in dist\KeySoundOverlay recursively
    Copy-Item -Path "dist\KeySoundOverlay\*" -Destination $TargetDir -Recurse -Force
} else {
    Write-Error "dist\KeySoundOverlay folder not found! Make sure to compile first."
    Exit
}

# 3. Create Desktop and Start Menu Shortcuts using COM object
Write-Host "Creating shortcuts..." -ForegroundColor Cyan
$WshShell = New-Object -ComObject WScript.Shell

# Desktop shortcut
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = "$TargetDir\KeySoundOverlay.exe"
$Shortcut.WorkingDirectory = $TargetDir
$Shortcut.Save()

# Start Menu shortcut
$ShortcutStart = $WshShell.CreateShortcut($StartMenuPath)
$ShortcutStart.TargetPath = "$TargetDir\KeySoundOverlay.exe"
$ShortcutStart.WorkingDirectory = $TargetDir
$ShortcutStart.Save()

# 4. Create Uninstaller script in the target directory
$UninstallScriptPath = "$TargetDir\uninstall.ps1"
$UninstallScriptContent = @"
`$AppName = "KeySoundOverlay"
`$TargetDir = "`$env:LOCALAPPDATA\Programs\`$AppName"

`$DesktopDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
`$ShortcutPath = Join-Path `$DesktopDir "KeySound Overlay.lnk"

`$StartMenuProgramsDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Programs)
`$StartMenuPath = Join-Path `$StartMenuProgramsDir "KeySound Overlay.lnk"

Write-Host "Uninstalling KeySound Overlay..." -ForegroundColor Yellow

# Remove Shortcuts
if (Test-Path `$ShortcutPath) { Remove-Item `$ShortcutPath -Force }
if (Test-Path `$StartMenuPath) { Remove-Item `$StartMenuPath -Force }

# Remove Registry Autostart
`$RegRunKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
if (Get-ItemProperty -Path `$RegRunKey -Name `$AppName -ErrorAction SilentlyContinue) {
    Remove-ItemProperty -Path `$RegRunKey -Name `$AppName -Force
}

# Remove Uninstall Registry Key
`$RegUninstallKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\`$AppName"
if (Test-Path `$RegUninstallKey) {
    Remove-Item -Path `$RegUninstallKey -Recurse -Force
}

# Remove directory (excluding this script)
if (Test-Path `$TargetDir) {
    Get-ChildItem -Path `$TargetDir -Exclude uninstall.ps1, uninstall.bat | Remove-Item -Recurse -Force
    # CMD self-deletion script scheduled after exit
    Start-Process cmd -ArgumentList "/c timeout /t 1 && rmdir /s /q `"`$TargetDir`"" -WindowStyle Hidden
}

Write-Host "Uninstall complete!" -ForegroundColor Green
"@
$UninstallScriptContent | Out-File -FilePath $UninstallScriptPath -Encoding utf8

# Create a cmd wrapper for uninstaller so Windows Add/Remove programs can run it easily
$UninstallCmdPath = "$TargetDir\uninstall.bat"
$UninstallCmdContent = "@echo off`r`npowershell -NoProfile -ExecutionPolicy Bypass -File `"%~dp0uninstall.ps1`"`r`n"
$UninstallCmdContent | Out-File -FilePath $UninstallCmdPath -Encoding ascii

# 5. Write Uninstall Registry Entries for Windows "Apps & Features"
Write-Host "Registering app in Windows Settings (Add/Remove Programs)..." -ForegroundColor Cyan
$RegUninstallPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\$AppName"
if (-not (Test-Path $RegUninstallPath)) {
    New-Item -Path $RegUninstallPath -Force | Out-Null
}
Set-ItemProperty -Path $RegUninstallPath -Name "DisplayName" -Value "KeySound Overlay"
Set-ItemProperty -Path $RegUninstallPath -Name "DisplayVersion" -Value "1.0.0"
Set-ItemProperty -Path $RegUninstallPath -Name "Publisher" -Value "KeySound Dev"
Set-ItemProperty -Path $RegUninstallPath -Name "UninstallString" -Value "`"$UninstallCmdPath`""
Set-ItemProperty -Path $RegUninstallPath -Name "DisplayIcon" -Value "$TargetDir\KeySoundOverlay.exe"

Write-Host "==============================================" -ForegroundColor Green
Write-Host "KeySound Overlay installed successfully!" -ForegroundColor Green
Write-Host "Check your Desktop or Start Menu!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Green
