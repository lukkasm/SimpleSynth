from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

from gui.keyboard import KeyboardMixin


class MainWindow(QWidget, KeyboardMixin):
    def __init__(self, engine):
        QWidget.__init__(self)
        self.engine = engine
        self.setWindowTitle("Simple Synth")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(400, 200)

    def on_key_down(self, note):
        self.engine.note_on(note)

    def on_key_up(self, note):
        self.engine.note_off()
