from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt

from gui.keyboard import KeyboardMixin
from gui.frequency_spectrum import FrequencySpectrum
from gui.oscillator_widget import OscillatorWidget
from gui.voice_tune_widget import TunerWidget


class MainWindow(QWidget, KeyboardMixin):
    def __init__(self, engine):
        QWidget.__init__(self)
        self.engine = engine
        self.setWindowTitle("Simple Synth")
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.resize(800, 400)

        # Main layout - vertical stack
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Add frequency spectrum widget on top
        self.spectrum = FrequencySpectrum(engine)
        main_layout.addWidget(self.spectrum)

        # Horizontal layout for OSC, tuner
        bottom_layout = QHBoxLayout()
        main_layout.addLayout(bottom_layout)

        # Add oscillator widget
        self.osc_widget = OscillatorWidget(self.engine.voice, self.engine)
        bottom_layout.addWidget(self.osc_widget)

        # Add tuner widget
        self.tuner_widget = TunerWidget(self.engine.voice.tuner)
        bottom_layout.addWidget(self.tuner_widget)

        self.tuner_widget.dial.valueChanged.connect(
            lambda _: self.engine.voice.update_frequency())


    # --- key events ---
    def on_key_down(self, note):
        "Play note on key down"
        self.engine.note_on(note)

    def on_key_up(self, note):
        "Stop note on key up"
        self.engine.note_off()
