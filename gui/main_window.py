from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from gui.keyboard import KeyboardMixin
from gui.frequency_spectrum import FrequencySpectrum


class MainWindow(QWidget, KeyboardMixin):
    def __init__(self, engine):
        QWidget.__init__(self)
        self.engine = engine
        self.setWindowTitle("Simple Synth")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(800, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.spectrum = FrequencySpectrum(engine)
        self.layout.addWidget(self.spectrum)

    # --- key events ---
    def on_key_down(self, note):
        self.engine.note_on(note)

    def on_key_up(self, note):
        self.engine.note_off()
