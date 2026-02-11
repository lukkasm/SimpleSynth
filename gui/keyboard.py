from PyQt6.QtCore import Qt


NOTE_MAP = {
    Qt.Key.Key_A: 69,  # A4 = 440 Hz
    Qt.Key.Key_W: 70,  # A#4/Bb4
    Qt.Key.Key_S: 71,  # B4
    Qt.Key.Key_E: 72,  # C5
    Qt.Key.Key_D: 73,  # C#5
    Qt.Key.Key_F: 74,  # D5
    Qt.Key.Key_T: 75,  # D#5
    Qt.Key.Key_G: 76,  # E5
}


class KeyboardMixin:
    """
    Keyboard events and Note mapping.
    """

    def keyPressEvent(self, event):
        "Play note on key down"
        if event.isAutoRepeat():
            return

        if event.key() in NOTE_MAP:
            self.on_key_down(NOTE_MAP[event.key()])

    def keyReleaseEvent(self, event):
        "Stop note on key up"
        if event.isAutoRepeat():
            return

        if event.key() in NOTE_MAP:
            self.on_key_up(NOTE_MAP[event.key()])
