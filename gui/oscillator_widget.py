from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDial, QLabel


class OscillatorWidget(QWidget):
    def __init__(self, voice, engine):
        super().__init__()
        self.voice = voice
        self.engine = engine

        layout = QVBoxLayout()
        self.setLayout(layout)

        # OSC label
        self.label = QLabel("sine")
        layout.addWidget(self.label)

        # Knob with 4 positions for selecting oscillator type
        self.dial = QDial()
        self.dial.setMinimum(0)
        self.dial.setMaximum(3)
        self.dial.setNotchesVisible(True)
        self.dial.setWrapping(False)
        self.dial.valueChanged.connect(self.on_change)
        layout.addWidget(self.dial)

        self.osc_map = {0: "sine", 1: "saw", 2: "square", 3: "triangle"}

    def on_change(self, value):
        osc_type = self.osc_map.get(value, "sine")
        self.label.setText(osc_type)
        self.voice.set_oscillator(osc_type)
        self.engine._update_recorder()
