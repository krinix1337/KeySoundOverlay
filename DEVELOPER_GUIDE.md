# 🛠️ Developer Guide — KeySound Overlay

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.5.1-0078d4?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/UI-PySide6%20%28Qt6%29-41cd52?style=for-the-badge&logo=qt&logoColor=white" alt="Qt6">
</p>

Полное руководство для разработчиков и продвинутых пользователей.  
Здесь описана архитектура проекта, создание кастомных тем, добавление звуков, работа с профилями и сборка `.exe`.

---

## 📑 Содержание

1. [Структура проекта](#1-структура-проекта)
2. [Настройка окружения разработки](#2-настройка-окружения-разработки)
3. [Архитектура приложения](#3-архитектура-приложения)
4. [Создание кастомных тем](#4-создание-кастомных-тем)
5. [Добавление новых свичей (звуков)](#5-добавление-новых-свичей-звуков)
6. [Добавление кастомных раскладок оверлея](#6-добавление-кастомных-раскладок-оверлея)
7. [Работа с профилями](#7-работа-с-профилями)
8. [Сборка .exe и инсталлятора](#8-сборка-exe-и-инсталлятора)
9. [Конфигурационные ключи](#9-конфигурационные-ключи)
10. [Решение частых проблем](#10-решение-частых-проблем)

---

## 1. Структура проекта

```
KeySoundOverlay/
│
├── main.py                    # Точка входа, инициализация всех компонентов
├── requirements.txt           # Python-зависимости
├── build.bat                  # Скрипт автоматической сборки (.exe)
├── setup.iss                  # Скрипт Inno Setup для создания установщика
├── KeySoundOverlay.spec       # Спецификация PyInstaller
│
├── app/
│   ├── config.py              # Настройки приложения (DEFAULT_SETTINGS, AppConfig)
│   ├── overlay_window.py      # Оверлей клавиатуры (KeyCap, OverlayWindow)
│   │                          # + Оверлей мыши (MouseWidget, MouseOverlayWindow)
│   ├── settings_window.py     # Окно настроек (sidebar-дизайн, все вкладки)
│   ├── sound_player.py        # Аудиодвижок (pygame, pitch-shift, WAV пул)
│   ├── keyboard_listener.py   # Глобальный хук клавиатуры (pynput)
│   ├── mouse_listener.py      # Глобальный хук мыши (pynput)
│   ├── themes.py              # QSS стили всех тем (dark/light/glass/neon + custom)
│   ├── profiles.py            # Менеджер профилей (сохранение/загрузка JSON)
│   ├── update_manager.py      # OTA-обновления (GitHub API, скачивание)
│   ├── update_dialog.py       # Диалог обновления (прогресс-бар, запуск установщика)
│   ├── tray.py                # Системный трей (иконка, меню)
│   ├── autostart.py           # Управление реестром автозапуска
│   └── utils.py               # Утилиты (пути, генератор дефолтного WAV)
│
└── assets/
    ├── icon.ico               # Иконка приложения
    ├── github_banner.jpg      # Баннер для README
    ├── default_click.wav      # Встроенный звук по умолчанию
    ├── cherry_mx_blue.wav     # Пресеты свичей...
    └── *.wav                  # (18 WAV файлов всего)
```

---

## 2. Настройка окружения разработки

### Требования
- **Windows 10 / 11** (64-bit)
- **Python 3.8+** (рекомендуется 3.10 или 3.11)
- **Git**

### Шаги

```bash
# 1. Клонировать репозиторий
git clone https://github.com/krinix1337/KeySoundOverlay.git
cd KeySoundOverlay

# 2. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Запустить приложение
python main.py
```

### requirements.txt

```
PySide6>=6.4.0
pygame>=2.1.0
pynput>=1.7.6
pyinstaller>=5.0
```

> [!NOTE]
> `pyinstaller` нужен только для сборки `.exe`. Для запуска из исходника он не требуется.

---

## 3. Архитектура приложения

```
main.py
  ├── AppConfig           — загрузка/сохранение settings.json
  ├── SoundPlayer         — аудиодвижок (pygame.mixer)
  ├── OverlayWindow       — оверлей клавиатуры (Qt Tool Window)
  ├── MouseOverlayWindow  — оверлей мыши (Qt Tool Window)
  ├── SettingsWindow      — окно настроек (QDialog, sidebar)
  ├── SystemTrayController— иконка и меню в трее
  ├── GlobalKeyboardListener (QThread) — pynput keyboard hook
  │     └── signals: key_pressed(str), key_released(str)
  └── GlobalMouseListener    (QThread) — pynput mouse hook
        └── signals: mouse_moved(int,int), mouse_clicked(str,bool), mouse_scrolled(int)
```

### Поток данных при нажатии клавиши

```
pynput hook (системный поток)
  → emit key_pressed("a")           # Qt Signal через QueuedConnection
  → OverlayWindow.set_key_state()   # обновление стилей в UI потоке
  → KeyCap.update_style()           # QSS + ripple анимация
  → SoundPlayer.play_click()        # pygame.mixer.Sound.play()
```

---

## 4. Создание кастомных тем

Есть два способа: через **UI** (без кода) и через **JSON-файл** (ручной).

---

### 4.1 Через интерфейс приложения (рекомендуется)

1. Открой **Настройки → Внешний вид**
2. Нажми **🎨 Создать кастомную тему…**
3. Выбери цвета для окон настроек и оверлея
4. Нажми **💾 Сохранить тему**

Файл темы автоматически сохранится в:
```
%APPDATA%\KeySoundOverlay\themes\<название_темы>.json
```

---

### 4.2 Вручную через JSON-файл

Создай файл по пути `%APPDATA%\KeySoundOverlay\themes\my_theme.json`:

```json
{
    "theme_display_name": "Моя тема",
    "settings_window": {
        "background":  "#1A1A2E",
        "text":        "#E0E0E0",
        "accent":      "#E94560",
        "card_bg":     "#16213E",
        "border":      "#0F3460"
    },
    "overlay": {
        "key_idle_bg":     "rgba(22, 33, 62, 180)",
        "key_idle_border": "rgba(15, 52, 96, 200)",
        "key_idle_text":   "#E0E0E0",
        "key_active_bg":   "#E94560",
        "key_active_border": "#FFFFFF",
        "key_active_text": "#FFFFFF",
        "key_radius":      6,
        "container_bg":    "rgba(26, 26, 46, 120)",
        "container_border": "#E94560"
    }
}
```

Перезапусти приложение — тема появится в списке.

---

### 4.3 Встроенная тема через код (для контрибьюторов)

Добавь статическую тему прямо в [`app/themes.py`](app/themes.py):

**Шаг 1** — Добавь QSS-стиль в словарь `THEME_SETTINGS_STYLE`:

```python
# app/themes.py
THEME_SETTINGS_STYLE["matrix"] = """
    QMainWindow, QDialog {
        background-color: #0D0D0D;
        color: #00FF41;
    }
    QWidget {
        font-family: "Courier New", monospace;
        font-size: 13px;
        color: #00FF41;
    }
    QPushButton {
        background-color: #001a00;
        border: 1px solid #00FF41;
        border-radius: 4px;
        padding: 6px 12px;
        color: #00FF41;
    }
    QPushButton:hover {
        background-color: #003300;
    }
    /* ... другие элементы */
"""
```

**Шаг 2** — Добавь стиль клавиш оверлея в функцию `get_overlay_key_qss()`:

```python
def get_overlay_key_qss(theme, highlight_color, is_pressed, opacity=1.0):
    # ...
    elif theme == "matrix":
        if is_pressed:
            return f"""
                QLabel {{
                    background-color: #00FF41;
                    color: #000000;
                    border: 1px solid #00FF41;
                    border-radius: 4px;
                    font-weight: bold;
                }}
            """
        else:
            return f"""
                QLabel {{
                    background-color: rgba(0, 26, 0, {int(opacity * 200)});
                    color: #00FF41;
                    border: 1px solid rgba(0, 255, 65, {int(opacity * 180)});
                    border-radius: 4px;
                }}
            """
```

**Шаг 3** — Зарегистрируй в выпадающем списке в [`app/settings_window.py`](app/settings_window.py):

```python
# в методе load_values()
self.combo_theme.addItem("Matrix (Зелёный хакер)", "matrix")
```

---

## 5. Добавление новых свичей (звуков)

### 5.1 Использование существующего WAV-файла

1. Скопируй WAV-файл в папку [`assets/`](assets/):
   ```
   assets/my_switch.wav
   ```

2. Зарегистрируй в [`app/settings_window.py`](app/settings_window.py) в методе `_build_sound_page()`:
   ```python
   self.combo_presets.addItem("Мой свич (описание)", "assets/my_switch.wav")
   ```

3. Готово — приложение поддерживает любой 16-bit PCM WAV файл с pitch-shift вариациями.

---

### 5.2 Генерация синтетического WAV через Python

Ниже шаблон для создания реалистичного звука свича программно:

```python
import math, struct

def generate_my_switch(sample_rate=44100):
    duration = 0.045        # длительность в секундах
    freq = 680              # основная частота (Гц)
    decay = 150             # скорость затухания (больше = быстрее)
    amplitude = 0.65        # громкость 0.0–1.0

    n = int(sample_rate * duration)

    # WAV-заголовок
    header = bytearray()
    header.extend(b'RIFF')
    header.extend(struct.pack('<I', 36 + n * 2))
    header.extend(b'WAVEfmt ')
    header.extend(struct.pack('<I', 16))   # chunk size
    header.extend(struct.pack('<H', 1))    # PCM
    header.extend(struct.pack('<H', 1))    # Mono
    header.extend(struct.pack('<I', sample_rate))
    header.extend(struct.pack('<I', sample_rate * 2))
    header.extend(struct.pack('<H', 2))    # block align
    header.extend(struct.pack('<H', 16))   # bits per sample
    header.extend(b'data')
    header.extend(struct.pack('<I', n * 2))

    data = bytearray()
    for i in range(n):
        t = i / sample_rate
        envelope = math.exp(-t * decay)

        # Основной тон + гармоники для реализма
        val = 32767 * amplitude * envelope * (
            math.sin(2 * math.pi * freq * t) * 0.75 +
            math.sin(2 * math.pi * freq * 2 * t) * 0.15 +
            math.sin(2 * math.pi * freq * 0.5 * t) * 0.10
        )
        data.extend(struct.pack('<h', max(-32768, min(32767, int(val)))))

    with open("assets/my_switch.wav", "wb") as f:
        f.write(bytes(header + data))
```

**Советы по параметрам:**

| Тип свича | freq (Гц) | decay | amplitude | duration (с) |
|---|---|---|---|---|
| Кликающий | 1100–1300 | 200–250 | 0.7–0.9 | 0.035–0.040 |
| Линейный тихий | 450–600 | 130–170 | 0.4–0.6 | 0.035–0.050 |
| Тактильный | 700–900 | 150–200 | 0.6–0.8 | 0.040–0.055 |
| Thock (резина) | 180–280 | 50–80 | 0.6–0.75 | 0.070–0.090 |
| Беззвучный | 250–350 | 160–200 | 0.2–0.35 | 0.025–0.035 |

---

## 6. Добавление кастомных раскладок оверлея

### Шаг 1 — Создай метод построения раскладки в `OverlayWindow`

```python
# app/overlay_window.py → класс OverlayWindow

def build_my_layout(self):
    """Моя кастомная игровая раскладка."""
    self.container_layout.setSpacing(6)

    # Ряд 1: клавиши Q W E R
    r1 = QHBoxLayout()
    r1.setSpacing(6)
    r1.addStretch()
    for letter in ["q", "w", "e", "r"]:
        key = KeyCap(letter, letter.upper())
        key.setFixedSize(45, 45)
        r1.addWidget(key)
        self.key_widgets[letter] = key
    r1.addStretch()
    self.container_layout.addLayout(r1)

    # Ряд 2: клавиши A S D F
    r2 = QHBoxLayout()
    r2.setSpacing(6)
    r2.addStretch()
    for letter in ["a", "s", "d", "f"]:
        key = KeyCap(letter, letter.upper())
        key.setFixedSize(45, 45)
        r2.addWidget(key)
        self.key_widgets[letter] = key
    r2.addStretch()
    self.container_layout.addLayout(r2)
```

### Шаг 2 — Зарегистрируй размер окна

```python
# app/overlay_window.py → метод get_layout_size()

elif mode == "my_layout":
    return (240, 110)   # (ширина, высота) в пикселях
```

### Шаг 3 — Добавь вызов в `reload_ui()`

```python
# app/overlay_window.py → метод reload_ui()

elif mode == "my_layout":
    self.build_my_layout()
```

### Шаг 4 — Добавь в выпадающий список настроек

```python
# app/settings_window.py → метод _build_overlay_page()

self.combo_mode.addItem("Моя раскладка (название)", "my_layout")
```

> [!TIP]
> В `KeyCap(key_id, display_text)`:
> - `key_id` — внутренний идентификатор клавиши (что приходит от pynput)
> - `display_text` — что отображается на кнопке оверлея
>
> Специальные `key_id`: `space`, `enter`, `backspace`, `tab`, `caps_lock`, `shift_l`, `shift_r`, `ctrl_l`, `ctrl_r`, `alt_l`, `alt_r`, `esc`, `win`, `up`, `down`, `left`, `right`, `f1`–`f12`

---

## 7. Работа с профилями

Профили реализованы в модуле [`app/profiles.py`](app/profiles.py) через класс `ProfileManager`.

### API модуля

```python
from app.profiles import ProfileManager

mgr = ProfileManager(app_data_dir)  # app_data_dir = %APPDATA%\KeySoundOverlay

# Список всех сохранённых профилей
names = mgr.list_profiles()         # → ["gaming", "streaming", "default"]

# Сохранить текущие настройки как профиль
mgr.save_profile("gaming", config.settings)

# Загрузить профиль → dict настроек
settings = mgr.load_profile("gaming")
for key, val in settings.items():
    config.set(key, val)

# Удалить профиль
mgr.delete_profile("gaming")

# Получить отображаемое название
display = mgr.get_display_name("gaming")  # → "Gaming Profile"
```

### Формат JSON-файла профиля

Каждый профиль хранится в `%APPDATA%\KeySoundOverlay\profiles\<slug>.json`:

```json
{
    "profile_display_name": "Gaming",
    "settings": {
        "sound_enabled": true,
        "sound_file": "assets/gateron_yellow.wav",
        "volume": 60,
        "overlay_enabled": true,
        "overlay_mode": "wasd",
        "theme": "neon",
        "key_highlight_color": "#00F0FF",
        "key_press_animation": true,
        "show_in_fullscreen": true,
        "overlay_opacity": 0.75
    }
}
```

Ты можешь создавать профили вручную — просто скопируй любой файл настроек и измени значения.

---

## 8. Сборка .exe и инсталлятора

### Требования для сборки

- [PyInstaller](https://pyinstaller.org/) `pip install pyinstaller`
- [Inno Setup 6](https://jrsoftware.org/isdl.php) (для создания установщика)

---

### 8.1 Автоматическая сборка (рекомендуется)

```bash
# Запустить скрипт сборки (очищает предыдущие артефакты)
build.bat
```

Скрипт выполнит:
1. Очистку папок `build/` и `dist/`
2. Компиляцию через PyInstaller с `KeySoundOverlay.spec`
3. Результат: папка `dist/KeySoundOverlay/`

---

### 8.2 Ручная сборка через PyInstaller

```bash
pyinstaller --noconfirm KeySoundOverlay.spec
```

Файл `KeySoundOverlay.spec` настроен на:
- Режим `onedir` (папка, не единый EXE) — нет ложных срабатываний антивируса
- Включение всех WAV-файлов из `assets/`
- Включение иконки `icon.ico`
- Консоль скрыта (`console=False`)

---

### 8.3 Создание установщика Inno Setup

1. Установить [Inno Setup 6](https://jrsoftware.org/isdl.php)
2. Открыть `setup.iss` в Inno Setup Compiler
3. Нажать **Compile** (`Ctrl+F9`)
4. Результат: `dist/KeySoundOverlay_Setup.exe`

**Ключевые параметры `setup.iss`:**

```ini
[Setup]
AppName=KeySound Overlay
AppVersion=1.5.1                          ; ← обновлять при каждом релизе
DefaultDirName={localappdata}\Programs\KeySoundOverlay
PrivilegesRequired=lowest                  ; без прав администратора
Compression=lzma2/max                      ; максимальное сжатие
```

> [!IMPORTANT]
> Перед сборкой убедись, что `AppVersion` в `setup.iss` совпадает с `CURRENT_VERSION` в `app/update_manager.py`. Несовпадение может вызвать бесконечные предложения об обновлении.

---

### 8.4 Обновление версии приложения (чеклист)

При выпуске новой версии обнови значения **в трёх местах**:

```python
# 1. app/update_manager.py
CURRENT_VERSION = "1.5.1"
```
```ini
# 2. setup.iss
AppVersion=1.5.1
```
```ini
# 3. KeySoundOverlay.spec (если указана версия)
# exe_name = 'KeySoundOverlay'
# version = '1.5.1'
```

---

## 9. Конфигурационные ключи

Все настройки хранятся в `%APPDATA%\KeySoundOverlay\settings.json`.

| Ключ | Тип | По умолчанию | Описание |
|---|---|---|---|
| `sound_enabled` | bool | `true` | Воспроизводить звуки |
| `sound_file` | str | `""` | Путь к WAV-файлу (пусто = встроенный клик) |
| `volume` | int | `80` | Громкость 0–100 |
| `pitch_randomize` | bool | `true` | Случайный pitch ±10% |
| `repeat_on_hold` | bool | `false` | Повторять при удержании |
| `overlay_enabled` | bool | `true` | Показывать оверлей клавиатуры |
| `overlay_unlocked` | bool | `false` | Разблокировать перетаскивание |
| `overlay_opacity` | float | `0.85` | Прозрачность 0.0–1.0 |
| `overlay_mode` | str | `"full"` | Режим: `full/wasd/osu/dota/custom/pressed` |
| `overlay_x` / `overlay_y` | int | `100/600` | Позиция оверлея |
| `key_highlight_color` | str | `"#0078D4"` | HEX-цвет подсветки клавиш |
| `custom_layout_keys` | str | `"q, w, e, r..."` | Клавиши для режима custom |
| `theme` | str | `"dark"` | Тема: `dark/light/glass/neon/<custom_id>` |
| `key_press_animation` | bool | `true` | Ripple-анимация при нажатии |
| `show_in_fullscreen` | bool | `false` | Показывать поверх полноэкранных приложений |
| `mouse_overlay_enabled` | bool | `true` | Показывать оверлей мыши |
| `mouse_overlay_show_coords` | bool | `true` | Показывать координаты X/Y |
| `mouse_overlay_show_clicks` | bool | `true` | Подсвечивать кнопки |
| `mouse_overlay_unlocked` | bool | `false` | Разблокировать перетаскивание мыши |
| `mouse_overlay_x` / `y` | int | `720/600` | Позиция оверлея мыши |
| `mouse_overlay_opacity` | float | `0.85` | Прозрачность оверлея мыши |
| `autostart` | bool | `false` | Автозапуск с Windows |
| `minimize_to_tray` | bool | `true` | Сворачивать в трей |
| `start_minimized` | bool | `false` | Запускать скрытым |
| `check_updates_on_startup` | bool | `true` | Проверять обновления при запуске |

---

## 10. Решение частых проблем

### Приложение не запускается / вылетает сразу

```bash
# Запусти из терминала для просмотра ошибок:
python main.py
```

Частые причины:
- Не установлены зависимости → `pip install -r requirements.txt`
- Уже запущена другая копия → завершить через диспетчер задач

---

### Звук не воспроизводится

1. Убедись, что `pygame` установлен: `pip show pygame`
2. Проверь, что звук включён в настройках (`Звук → Включить воспроизведение`)
3. Проверь путь к WAV-файлу — файл должен существовать

---

### Оверлей не отображается поверх игры

- В настройках **Оверлей → Эффекты** включи **"Показывать поверх полноэкранных приложений"**
- Для эксклюзивного DirectX fullscreen это работает только с некоторыми играми
- Большинство современных игр используют borderless fullscreen — оверлей работает корректно

---

### PyInstaller собирает, но .exe не находит assets/

Убедись, что в `KeySoundOverlay.spec` правильно указаны данные:

```python
datas=[
    ('assets', 'assets'),   # копировать папку assets целиком
    ('app', 'app'),
],
```

---

<p align="center">
  <b>KeySound Overlay v1.5.1</b><br>
  <a href="README.md">← Назад к README</a> ·
  <a href="https://github.com/krinix1337/KeySoundOverlay/issues">🐛 Сообщить о баге</a> ·
  <a href="https://github.com/krinix1337/KeySoundOverlay/releases">⬇️ Релизы</a>
</p>
