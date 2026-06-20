@echo off
echo ==============================================
echo Building KeySound Overlay Executable
echo ==============================================

echo [1/3] Installing requirements...
pip install -r requirements.txt

echo [2/3] Generating default sound asset...
python -c "import os, sys; sys.path.append(os.getcwd()); from app.utils import generate_default_click; os.makedirs('assets', exist_ok=True); f=open('assets/default_click.wav','wb'); f.write(generate_default_click()); f.close(); print('Default WAV asset generated at assets/default_click.wav')"

echo [3/3] Compiling standalone executable via PyInstaller...
pyinstaller --noconfirm --onefile --windowed --name="KeySoundOverlay" --add-data "assets;assets" main.py

echo ==============================================
echo Build Completed successfully!
echo Executable is located in the "dist" folder:
echo key_sound_overlay\dist\KeySoundOverlay.exe
echo ==============================================
pause
