# app/mouse_listener.py
from PySide6.QtCore import QObject, Signal
from pynput import mouse

class GlobalMouseListener(QObject):
    mouse_moved = Signal(int, int)      # Emits (x, y) coordinates
    mouse_clicked = Signal(str, bool)   # Emits (button_name, is_pressed)
    mouse_scrolled = Signal(int)        # Emits scroll direction (+1 or -1)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.listener = None

    def start(self):
        """Starts the global mouse hook listener."""
        if self.listener is None:
            self.listener = mouse.Listener(
                on_move=self._on_move,
                on_click=self._on_click,
                on_scroll=self._on_scroll,
                suppress=False
            )
            self.listener.daemon = True
            self.listener.start()

    def stop(self):
        """Stops the global mouse hook listener."""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

    def _on_move(self, x, y):
        if self.config.get("mouse_overlay_enabled"):
            self.mouse_moved.emit(int(x), int(y))

    def _on_click(self, x, y, button, pressed):
        if self.config.get("mouse_overlay_enabled"):
            btn_name = "unknown"
            if button == mouse.Button.left:
                btn_name = "left"
            elif button == mouse.Button.right:
                btn_name = "right"
            elif button == mouse.Button.middle:
                btn_name = "middle"
            elif button == mouse.Button.x1:
                btn_name = "x1"
            elif button == mouse.Button.x2:
                btn_name = "x2"
            else:
                btn_name = str(button).split('.')[-1]

            self.mouse_clicked.emit(btn_name, pressed)

    def _on_scroll(self, x, y, dx, dy):
        if self.config.get("mouse_overlay_enabled"):
            direction = 1 if dy > 0 else -1
            self.mouse_scrolled.emit(direction)
