from PyQt6.QtCore import Qt


NOTE_MAP = {
    Qt.Key.Key_A: 30,
    Qt.Key.Key_W: 31,
    Qt.Key.Key_S: 32,
    Qt.Key.Key_E: 33,
    Qt.Key.Key_D: 34,
    Qt.Key.Key_F: 35,
    Qt.Key.Key_T: 36,
    Qt.Key.Key_G: 37,
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
