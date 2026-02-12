from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt

from gui.input.keyboard import KeyboardMixin
from gui.vizualization_window.frequency_spectrum import FrequencySpectrum
from gui.oscillator_widget.oscillator_widget import OscillatorWidget


class MainWindow(QWidget, KeyboardMixin):
    def __init__(self, engine):
        QWidget.__init__(self)
        self.engine = engine
        self.setWindowTitle("Simple Synth")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(1000, 500)

        # Main layout - vertical stack
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Add frequency spectrum widget on top
        self.spectrum = FrequencySpectrum(engine)
        main_layout.addWidget(self.spectrum)

        # Horizontal layout for OSC, tuner
        self.osc1_widget = OscillatorWidget(
            self.engine.voice.layer1, self.engine)
        main_layout.addWidget(self.osc1_widget)

        self.osc2_widget = OscillatorWidget(
            self.engine.voice.layer2, self.engine)
        main_layout.addWidget(self.osc2_widget)


    # --- key events ---
    def on_key_down(self, note):
        "Play note on key down"
        self.engine.note_on(note)

    def on_key_up(self, note):
        "Stop note on key up"
        self.engine.note_off()
