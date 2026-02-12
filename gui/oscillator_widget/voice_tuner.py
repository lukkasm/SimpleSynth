from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDial, QLabel
from PyQt6.QtCore import Qt


class VoiceTuner(QWidget):
    """
    QDial widget for semitone tuning.
    """

    def __init__(self, tuner):
        super().__init__()
        self.tuner = tuner

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel(f"Tune: {self.tuner.semitone_offset} semitones")
        layout.addWidget(self.label)

        self.dial = QDial()
        self.dial.setMinimum(-24)   # one octave down
        self.dial.setMaximum(24)    # one octave up
        self.dial.setNotchesVisible(True)
        self.dial.setWrapping(False)
        self.dial.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.dial.valueChanged.connect(self.on_change)
        layout.addWidget(self.dial)

    def on_change(self, value):
        self.tuner.set_semitone_offset(value)
        self.label.setText(f"Tune: {value} semitones")
