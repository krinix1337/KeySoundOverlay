# app/icons.py
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QByteArray

_ICON_CACHE = {}

_SVG_DATA = {
    "sound": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M11 4.702a.705.705 0 0 0-1.203-.498L6.413 7.587A1.4 1.4 0 0 1 5.416 8H3a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2.416a1.4 1.4 0 0 1 .997.413l3.383 3.384A.705.705 0 0 0 11 19.298z" />
  <path d="M16 9a5 5 0 0 1 0 6" />
  <path d="M19.364 18.364a9 9 0 0 0 0-12.728" />
</svg>
""",
    "keyboard": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M10 8h.01" />
  <path d="M12 12h.01" />
  <path d="M14 8h.01" />
  <path d="M16 12h.01" />
  <path d="M18 8h.01" />
  <path d="M6 8h.01" />
  <path d="M7 16h10" />
  <path d="M8 12h.01" />
  <rect width="20" height="16" x="2" y="4" rx="2" />
</svg>
""",
    "palette": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M12 22a1 1 0 0 1 0-20 10 9 0 0 1 10 9 5 5 0 0 1-5 5h-2.25a1.75 1.75 0 0 0-1.4 2.8l.3.4a1.75 1.75 0 0 1-1.4 2.8z" />
  <circle cx="13.5" cy="6.5" r=".5" fill="currentColor" />
  <circle cx="17.5" cy="10.5" r=".5" fill="currentColor" />
  <circle cx="6.5" cy="12.5" r=".5" fill="currentColor" />
  <circle cx="8.5" cy="7.5" r=".5" fill="currentColor" />
</svg>
""",
    "profile": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
  <circle cx="12" cy="7" r="4" />
</svg>
""",
    "settings": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M9.671 4.136a2.34 2.34 0 0 1 4.659 0 2.34 2.34 0 0 0 3.319 1.915 2.34 2.34 0 0 1 2.33 4.033 2.34 2.34 0 0 0 0 3.831 2.34 2.34 0 0 1-2.33 4.033 2.34 2.34 0 0 0-3.319 1.915 2.34 2.34 0 0 1-4.659 0 2.34 2.34 0 0 0-3.32-1.915 2.34 2.34 0 0 1-2.33-4.033 2.34 2.34 0 0 0 0-3.831A2.34 2.34 0 0 1 6.35 6.051a2.34 2.34 0 0 0 3.319-1.915" />
  <circle cx="12" cy="12" r="3" />
</svg>
""",
    "play": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M5 5a2 2 0 0 1 3.008-1.728l11.997 6.998a2 2 0 0 1 .003 3.458l-12 7A2 2 0 0 1 5 19z" />
</svg>
""",
    "folder": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z" />
</svg>
""",
    "save": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M15.2 3a2 2 0 0 1 1.4.6l3.8 3.8a2 2 0 0 1 .6 1.4V19a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2z" />
  <path d="M17 21v-7a1 1 0 0 0-1-1H8a1 1 0 0 0-1 1v7" />
  <path d="M7 3v4a1 1 0 0 0 1 1h7" />
</svg>
""",
    "trash": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M10 11v6" />
  <path d="M14 11v6" />
  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6" />
  <path d="M3 6h18" />
  <path d="M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
</svg>
""",
    "load": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="m6 14 1.5-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.54 6a2 2 0 0 1-1.95 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2" />
</svg>
""",
    "refresh": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
  <path d="M21 3v5h-5" />
  <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
  <path d="M8 16H3v5" />
</svg>
""",
    "search": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="m21 21-4.34-4.34" />
  <circle cx="11" cy="11" r="8" />
</svg>
""",
    "check": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M20 6 9 17l-5-5" />
</svg>
""",
    "update": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M12 15V3" />
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
  <path d="m7 10 5 5 5-5" />
</svg>
""",
    "plus": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M5 12h14" />
  <path d="M12 5v14" />
</svg>
""",
    "warning": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" />
  <path d="M12 9v4" />
  <path d="M12 17h.01" />
</svg>
""",
    "resize": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <path d="M8 3H5a2 2 0 0 0-2 2v3" />
  <path d="M21 8V5a2 2 0 0 0-2-2h-3" />
  <path d="M3 16v3a2 2 0 0 0 2 2h3" />
  <path d="M16 21h3a2 2 0 0 0 2-2v-3" />
</svg>
""",
    "snap": """<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{size}"
  height="{size}"
  viewBox="0 0 24 24"
  fill="none"
  stroke="{color}"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <circle cx="12" cy="12" r="10" />
  <line x1="22" x2="18" y1="12" y2="12" />
  <line x1="6" x2="2" y1="12" y2="12" />
  <line x1="12" x2="12" y1="6" y2="2" />
  <line x1="12" x2="12" y1="22" y2="18" />
</svg>
""",
}

def get_icon(name: str, color: str = "#E2E2E2", size: int = 20) -> QIcon:
    key = (name, color, size)
    if key not in _ICON_CACHE:
        svg_template = _SVG_DATA.get(name)
        if svg_template:
            svg = svg_template.format(color=color, size=size)
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(svg.encode('utf-8')), "SVG")
            _ICON_CACHE[key] = QIcon(pixmap)
        else:
            _ICON_CACHE[key] = QIcon()
    return _ICON_CACHE[key]
