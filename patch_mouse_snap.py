import re

with open('app/overlay_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_mouse_move_mouse = '''    def mouseMoveEvent(self, event):
        if self.config.get("mouse_overlay_unlocked") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()'''

new_mouse_move_mouse = '''    def mouseMoveEvent(self, event):
        if self.config.get("mouse_overlay_unlocked") and event.buttons() == Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            
            # Snapping logic
            screen = self.screen().geometry()
            snap_dist = 25
            
            center_x = new_pos.x() + self.width() // 2
            center_y = new_pos.y() + self.height() // 2
            
            sc_x = screen.center().x()
            sc_y = screen.center().y()
            
            if abs(center_x - sc_x) < snap_dist:
                new_pos.setX(sc_x - self.width() // 2)
            if abs(center_y - sc_y) < snap_dist:
                new_pos.setY(sc_y - self.height() // 2)
                
            self.move(new_pos)
            event.accept()'''

if old_mouse_move_mouse in code:
    code = code.replace(old_mouse_move_mouse, new_mouse_move_mouse)
    with open('app/overlay_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("MouseOverlayWindow snapping patched successfully.")
else:
    print("Could not find MouseOverlayWindow mouseMoveEvent!")
