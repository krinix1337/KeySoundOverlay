import urllib.request, json, os

lucide_url = 'https://raw.githubusercontent.com/lucide-icons/lucide/main/icons/'
icons_to_fetch = {
    'sound': 'volume-2.svg',
    'keyboard': 'keyboard.svg',
    'palette': 'palette.svg',
    'profile': 'user.svg',
    'settings': 'settings.svg',
    'play': 'play.svg',
    'folder': 'folder.svg',
    'save': 'save.svg',
    'trash': 'trash-2.svg',
    'load': 'folder-open.svg',
    'refresh': 'refresh-cw.svg',
    'search': 'search.svg',
    'check': 'check.svg',
    'update': 'download.svg',
    'plus': 'plus.svg',
    'warning': 'triangle-alert.svg',
    'resize': 'maximize.svg',
    'snap': 'crosshair.svg'
}

svg_data = {}
for name, filename in icons_to_fetch.items():
    url = lucide_url + filename
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            svg_text = resp.read().decode('utf-8')
            svg_text = svg_text.replace('stroke="currentColor"', 'stroke="{color}"')
            svg_text = svg_text.replace('width="24"', 'width="{size}"')
            svg_text = svg_text.replace('height="24"', 'height="{size}"')
            svg_data[name] = svg_text
            print('Fetched', name)
    except Exception as e:
        print('Failed', name, e)

code = '''# app/icons.py
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QByteArray

_ICON_CACHE = {}

_SVG_DATA = {
'''
for name, svg in svg_data.items():
    code += f'    "{name}": """{svg}""",\n'
code += '''}

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
'''

with open('app/icons.py', 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated app/icons.py')
