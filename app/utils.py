import os
import sys
import math
import struct

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.join(base_path, relative_path)

def generate_default_click():
    """Generates a high-quality 16-bit PCM Mono WAV file of a click sound in bytes."""
    sample_rate = 44100
    duration = 0.04  # 40 ms duration - short and crisp click
    frequency = 900  # 900 Hz sine wave
    num_samples = int(sample_rate * duration)
    
    # WAV header construction
    header = bytearray()
    header.extend(b'RIFF')
    header.extend(struct.pack('<I', 36 + num_samples * 2))
    header.extend(b'WAVEfmt ')
    header.extend(struct.pack('<I', 16)) # Subchunk1Size
    header.extend(struct.pack('<H', 1))  # AudioFormat (PCM = 1)
    header.extend(struct.pack('<H', 1))  # NumChannels (1 = Mono)
    header.extend(struct.pack('<I', sample_rate)) # SampleRate
    header.extend(struct.pack('<I', sample_rate * 2)) # ByteRate
    header.extend(struct.pack('<H', 2))  # BlockAlign
    header.extend(struct.pack('<H', 16)) # BitsPerSample
    header.extend(b'data')
    header.extend(struct.pack('<I', num_samples * 2))
    
    # Audio samples construction
    data = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        # Rapid exponential decay for mechanical feel
        envelope = math.exp(-t * 120)
        # Combine a primary frequency with a high pitch click transient
        val = int(32767 * math.sin(2 * math.pi * frequency * t) * envelope)
        data.extend(struct.pack('<h', val))
        
    return bytes(header + data)

def get_app_icon():
    """Returns application QIcon. Tries to load assets/icon.ico, generates fallback if missing."""
    from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
    from PySide6.QtCore import Qt
    icon_path = get_resource_path("assets/icon.ico")
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    
    # Programmatic fluent-style icon fallback
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Accent background
    painter.setBrush(QColor("#0078D4"))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
    
    # Overlay text
    painter.setPen(QColor("#FFFFFF"))
    font = QFont("Segoe UI", 18, QFont.Bold)
    painter.setFont(font)
    painter.drawText(pixmap.rect(), Qt.AlignCenter, "KS")
    
    painter.end()
    return QIcon(pixmap)
