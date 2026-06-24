import re

with open('app/overlay_window.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_mouse_move = '''    def mouseMoveEvent(self, event):
        if self.config.get("overlay_unlocked") and event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()'''

new_mouse_move = '''    def mouseMoveEvent(self, event):
        if self.config.get("overlay_unlocked") and event.buttons() == Qt.LeftButton:
            new_pos = event.globalPosition().toPoint() - self.drag_position
            
            # Snapping logic
            screen = self.screen().geometry()
            snap_dist = 25
            
            # Center of the overlay
            center_x = new_pos.x() + self.width() // 2
            center_y = new_pos.y() + self.height() // 2
            
            # Screen centers
            sc_x = screen.center().x()
            sc_y = screen.center().y()
            
            # Magnetize to center X
            if abs(center_x - sc_x) < snap_dist:
                new_pos.setX(sc_x - self.width() // 2)
            
            # Magnetize to center Y
            if abs(center_y - sc_y) < snap_dist:
                new_pos.setY(sc_y - self.height() // 2)
                
            self.move(new_pos)
            event.accept()'''

if old_mouse_move in code:
    code = code.replace(old_mouse_move, new_mouse_move)
    with open('app/overlay_window.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Overlay snapping patched successfully.")
else:
    print("Could not find old mouseMoveEvent code to patch!")

