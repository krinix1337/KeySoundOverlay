# KeySound Overlay

<p align="center">
  <img src="assets/github_banner.jpg" alt="KeySound Overlay Banner" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Version-1.3.0-0078d4?style=for-the-badge&logo=github" alt="Version">
  <img src="https://img.shields.io/badge/OS-Windows%2010%20%7C%2011-0078d4?style=for-the-badge&logo=windows" alt="Windows">
  <img src="https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/UI-PySide6%20%28Qt6%29-41cd52?style=for-the-badge&logo=qt&logoColor=white" alt="Qt6">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="License">
</p>

<p align="center">
  <b>Overlay клавиатуры и мыши с живыми звуками механических свичей для Windows</b><br>
  <i>Fluent Design · Профили · Анимации · Полноэкранный режим · OTA-обновления</i>
</p>

---

> [!IMPORTANT]
> Приложение использует низкоуровневый системный hook **исключительно** для подсветки клавиш и воспроизведения звуков. Никакой введённый текст не сохраняется, не логируется и не передаётся по сети.

---

## 📖 Документация

| Документ | Описание |
|---|---|
| 📄 **[README.md](README.md)** | Описание, установка, список свичей — вы здесь |
| 🛠️ **[DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)** | Темы, сборка, пресеты, архитектура, профили |

---

## ✨ Возможности

<table>
<tr>
<td width="50%">

**🎹 Звук механических свичей**
- 18 встроенных пресетов свичей
- Pitch-shift ±10% для органичного звука
- Поддержка WAV / MP3 / OGG файлов
- Задержка < 5ms (pygame.mixer, буфер 512б)

**⌨️ Оверлей клавиатуры**
- 6 режимов: Full / WASD / Osu! / Dota2 / Custom / Pressed
- Ripple-анимация при нажатии клавиш
- Click-through (клики проходят сквозь оверлей)
- Лог комбинаций клавиш с учётом раскладки

</td>
<td width="50%">

**🖱️ Оверлей мыши**
- Визуализация кнопок мыши (LMB / RMB / MMB / X1 / X2)
- Координаты X/Y в реальном времени
- Колёсико прокрутки с анимацией

**⚙️ Система**
- 4 встроенные темы + конструктор кастомных тем
- Профили настроек (сохранять / загружать / удалять)
- Показывать поверх полноэкранных приложений
- OTA-обновления с GitHub Releases
- Автозапуск, трей, одна копия

</td>
</tr>
</table>

---

## 🔊 Все свичи (18 пресетов)

### Классика
| Свич | Тип | Звук |
|---|---|---|
| **Cherry MX Blue** | Кликающий | Громкий чёткий щелчок |
| **Cherry MX Brown** | Тактильный | Мягкий средний клик |
| **Cherry MX Red** | Линейный | Тихий плавный ход |
| **Cherry MX Black** | Линейный (тяжёлый) | Глубокий плотный звук |
| **Holy Panda** | Тактильный | Легендарный THOCK |
| **Turquoise Tealio** | Линейный | Глубокий чистый CLACK |
| **NovelKeys Cream** | Линейный | Гладкий деревянный стук |
| **Cream Travel** | Линейный (тихий) | Мягкий укороченный ход |
| **EG Oreo** | Тактильный | Песочный глухой стук |
| **Crystal Purple** | Тактильный | Звонкий яркий щелчок |
| **Topre Purple Hybrid** | Электроёмкостный | Премиальный глухой thock |

### Новые свичи (v1.3.0)
| Свич | Тип | Звук |
|---|---|---|
| 🟡 **Gateron Yellow** | Линейный | Ультра-тихий гладкий ход |
| 🟠 **Alps SKCM Orange** | Тактильный | Винтажный двойной удар |
| ⬜ **Kailh Box White** | Кликающий | Чёткий box-клик с резонансом |
| ⚡ **Speed Silver** | Линейный | Сверхкороткий быстрый ход |
| 🔵 **Topre 45g** | Электроёмкостный | Глубокий низкочастотный thock |
| 🔇 **Boba U4 Silent** | Тактильный (тихий) | Беззвучный мягкий ход |
| 🩷 **Akko CS Jelly Pink** | Тактильный | Гладкий с лёгкими гармониками |

---

## 🎨 Темы оформления

| Тема | Описание |
|---|---|
| **Dark** | Тёмная Fluent — стандарт Windows 11 |
| **Light** | Светлая Fluent — чистая и контрастная |
| **Glass** | Эффект матового стекла с тонкими рамками |
| **Neon Blue** | Киберпанк-стиль с неоновой подсветкой |
| **Кастомные** | Создай свою через Настройки → Внешний вид → Создать тему |

---

## 🚀 Установка

### ⚡ Быстро — скачать готовый установщик

1. Перейди в раздел **[Releases](https://github.com/krinix1337/KeySoundOverlay/releases)** на GitHub
2. Скачай `KeySoundOverlay_Setup.exe` из последнего релиза
3. Запусти установщик — он не требует прав администратора

### 🐍 Из исходного кода

```bash
# Клонировать репозиторий
git clone https://github.com/krinix1337/KeySoundOverlay.git
cd KeySoundOverlay

# Установить зависимости
pip install -r requirements.txt

# Запустить
python main.py
```

> [!TIP]
> Рекомендуется Python 3.10+ и виртуальное окружение (`python -m venv venv`)

---

## 🖥️ Режимы оверлея

| Режим | Размер | Описание |
|---|---|---|
| `full` | 610×215 | Полная ANSI-клавиатура |
| `wasd` | 270×140 | WASD + Shift + Space + Ctrl |
| `osu` | 150×140 | Z + X + Space + Esc |
| `dota` | 340×170 | Скиллы + предметы + модификаторы |
| `custom` | динамический | Любые клавиши через запятую |
| `pressed` | 500×60 | Лог нажатых клавиш и комбинаций |

---

## 👤 Профили

Профили позволяют переключаться между разными наборами настроек.  
Создаются в **Настройки → Профили → 💾 Сохранить текущий**

- Хранятся в `%APPDATA%\KeySoundOverlay\profiles\`
- Каждый профиль — JSON-файл с полным снимком настроек

---

## 🔄 Обновления

KeySound Overlay проверяет обновления автоматически при запуске (настраивается).  
При наличии новой версии на GitHub Releases — появляется диалог с описанием изменений и кнопкой «Обновить».

---

## 📋 Системная информация

```
Настройки:   %APPDATA%\KeySoundOverlay\settings.json
Профили:     %APPDATA%\KeySoundOverlay\profiles\
Темы:        %APPDATA%\KeySoundOverlay\themes\
Автозапуск:  HKCU:\Software\Microsoft\Windows\CurrentVersion\Run\KeySoundOverlay
Удаление:    Параметры Windows → Приложения → KeySound Overlay
```

---

## 🛠️ Для разработчиков

Полное руководство по разработке, кастомизации и сборке:  
**→ [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)**

Там описано:
- Структура проекта и архитектура
- Как создавать кастомные темы (JSON + QSS)
- Как добавлять новые свичи
- Как собрать `.exe` и инсталлятор
- Как публиковать релизы для OTA-обновлений
- Как работать с профилями

---

## 📄 Лицензия

MIT License — см. файл `LICENSE`.

---

<p align="center">
  Сделано с ❤️ для механических энтузиастов<br>
  <a href="https://github.com/krinix1337/KeySoundOverlay/releases">⬇️ Скачать</a> ·
  <a href="https://github.com/krinix1337/KeySoundOverlay/issues">🐛 Баги</a> ·
  <a href="DEVELOPER_GUIDE.md">📖 Документация</a>
</p>
