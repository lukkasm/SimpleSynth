from PyQt6.QtCore import Qt


NOTE_MAP = {
    Qt.Key.Key_A: 60,
    Qt.Key.Key_W: 61,
    Qt.Key.Key_S: 62,
    Qt.Key.Key_E: 63,
    Qt.Key.Key_D: 64,
    Qt.Key.Key_F: 65,
    Qt.Key.Key_G: 66,
}


class KeyboardMixin:
    """
    Keyboard events and Note mapping.
    """

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() in NOTE_MAP:
            self.on_key_down(NOTE_MAP[event.key()])

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return

        if event.key() in NOTE_MAP:
            self.on_key_up(NOTE_MAP[event.key()])
