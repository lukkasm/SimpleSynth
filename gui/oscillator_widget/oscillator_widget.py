from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from gui.oscillator_widget.oscillator import Oscillator
from gui.oscillator_widget.voice_tuner import VoiceTuner
from gui.oscillator_widget.adsr import ADSR


class OscillatorWidget(QWidget):
    """Encapsulates one oscillator layer: Oscillator + Tuner + ADSR"""

    def __init__(self, layer, engine, layer_name="Oscillator"):
        super().__init__()
        self.layer = layer
        self.engine = engine

        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel(layer_name))

        # Oscillator widget
        self.osc_widget = Oscillator(layer, engine)
        layout.addWidget(self.osc_widget)

        # Tuner widget
        self.tuner_widget = VoiceTuner(layer.tuner)
        layout.addWidget(self.tuner_widget)
        self.tuner_widget.dial.valueChanged.connect(layer.update_frequency)

        # ADSR widget
        self.adsr_widget = ADSR(layer.env)
        layout.addWidget(self.adsr_widget)
