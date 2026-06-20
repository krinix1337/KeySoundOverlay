# 🛠️ Руководство по кастомизации и разработке (KeySound Overlay)

Это руководство предназначено для разработчиков и пользователей, которые хотят настроить приложение под себя: добавить свои раскладки клавиатуры, пресеты звуков, новые темы оформления или скомпилировать проект самостоятельно.

---

## 1. Добавление кастомных раскладок оверлея
Вся логика построения клавиш находится в файле [overlay_window.py](file:///C:/project/key_sound_overlay/app/overlay_window.py).

Чтобы добавить новый режим отображения (раскладку):
1.  **Создайте метод построения раскладки** в классе `OverlayWindow` (по аналогии с `build_wasd_layout`):
    ```python
    def build_my_custom_layout(self):
        self.container_layout.setSpacing(6)
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addStretch()
        
        # Добавляем клавишу Z
        z_key = KeyCap("z", "Z")
        z_key.setFixedSize(45, 45)
        row.addWidget(z_key)
        self.key_widgets["z"] = z_key
        
        row.addStretch()
        self.container_layout.addLayout(row)
    ```
2.  **Зарегистрируйте размер окна** для вашего режима в методе `get_layout_size(self)`:
    ```python
    elif mode == "my_custom":
        return (100, 100) # Ширина, Высота в пикселях
    ```
3.  **Добавьте вызов вашего метода** в `reload_ui(self)`:
    ```python
    elif mode == "my_custom":
        self.build_my_custom_layout()
    ```
4.  **Добавьте вариант выбора** в выпадающий список настроек в файле [settings_window.py](file:///C:/project/key_sound_overlay/app/settings_window.py):
    ```python
    self.combo_mode.addItem("Моя раскладка", "my_custom")
    ```

---

## 2. Добавление новых звуковых пресетов (свитчей)
Приложение поддерживает воспроизведение любых звуковых файлов формата `.wav` с низкой задержкой.

1.  **Скопируйте ваш аудиофайл** в папку [assets/](file:///C:/project/key_sound_overlay/assets/) (например, `assets/my_switch_sound.wav`).
2.  **Зарегистрируйте свич в настройках** в файле [settings_window.py](file:///C:/project/key_sound_overlay/app/settings_window.py) внутри метода `build_sound_tab()` в выпадающем списке пресетов:
    ```python
    self.combo_presets.addItem("Мой кастомный свич", "my_switch_sound.wav")
    ```
3.  **Обновите таблицу свитчей** в `README.md`, чтобы пользователи знали о новом пресете.

---

## 3. Настройка кастомных тем оформления
Стили окон настроек и кнопок оверлея используют QSS (аналог CSS для Qt-приложений).

*   Стили окон настроек определены в словаре `THEME_SETTINGS_STYLE` в файле [themes.py](file:///C:/project/key_sound_overlay/app/themes.py).
*   Стили клавиш оверлея возвращаются функцией `get_overlay_key_qss()`.

Вы можете добавить новую статическую тему (например, `matrix`):
1.  Добавьте QSS стили в `THEME_SETTINGS_STYLE`:
    ```python
    "matrix": """
        QMainWindow, QDialog {
            background-color: #000000;
            color: #00FF00;
        }
        ...
    """
    ```
2.  Настройте внешний вид кнопок оверлея в `get_overlay_key_qss()` для темы `matrix`.
3.  Добавьте пункт выбора темы в `self.combo_theme` в [settings_window.py](file:///C:/project/key_sound_overlay/app/settings_window.py):
    ```python
    self.combo_theme.addItem("Matrix (Зеленый хакер)", "matrix")
    ```

---

## 4. Сборка исполняемых файлов (.exe) и установщика
Для сборки проекта на Windows используются PyInstaller и Inno Setup.

### Шаг 1: Компиляция Python-кода
Мы компилируем приложение в режиме директории (`--onedir`), чтобы обойти проблемы с блокировкой папки `%TEMP%` антивирусами.
Выполните скрипт автоматической сборки в консоли:
```bash
build.bat
```
*Этот скрипт очистит предыдущие сборки, запустит PyInstaller с файлом спецификации `KeySoundOverlay.spec` и подготовит файлы в папке `dist/KeySoundOverlay/`.*

### Шаг 2: Создание файла установки (`KeySoundOverlay_Setup.exe`)
Для создания профессионального установщика:
1.  Установите [Inno Setup Compiler](https://jrsoftware.org/isdl.php).
2.  Откройте файл `setup.iss` в Inno Setup Compiler и нажмите кнопку **Compile** (или нажмите `Ctrl + F9`).
3.  На выходе в папке `dist/` появится файл `KeySoundOverlay_Setup.exe`.

---

## 5. Публикация обновлений на GitHub (для работы автообновлений)
После реализации функции OTA (обновления по воздуху), ваше приложение будет сверять свою версию с релизами на GitHub.

Чтобы выпустить обновление, которое автоматически придет всем пользователям:
1.  **Обновите версию в коде** в файле `app/update_manager.py` (измените константу `CURRENT_VERSION`, например, на `"1.1.0"`).
2.  Скомпилируйте код и соберите установщик `KeySoundOverlay_Setup.exe`.
3.  Залейте обновленный исходный код в ваш репозиторий на GitHub.
4.  Перейдите во вкладку **Releases** на вашем GitHub и нажмите **Draft a new release**:
    *   Укажите тег версии, соответствующий коду (например, `v1.1.0`).
    *   Заполните описание изменений.
    *   Прикрепите скомпилированный файл `KeySoundOverlay_Setup.exe` в поле файлов релиза.
    *   Опубликуйте релиз (**Publish release**).

*При следующем запуске приложения у пользователей сработает проверка обновлений, и им будет предложено установить версию v1.1.0.*
