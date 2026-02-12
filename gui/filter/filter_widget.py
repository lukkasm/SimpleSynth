from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDial, QComboBox
from PyQt6.QtCore import Qt
import math


class FilterWidget(QWidget):
    FILTER_TYPES = ["low_pass", "band_pass", "high_pass", "notch"]

    def __init__(self, voice):
        super().__init__()
        self.voice = voice

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.addWidget(QLabel("Filter"))

        # --- Frequency knob ---
        freq_layout = QVBoxLayout()
        freq_layout.addWidget(QLabel("Frequency"))

        self.frequency_knob = QDial()
        self.frequency_knob.setMinimum(0)
        self.frequency_knob.setMaximum(100)  # use a 0-100 scale for dial
        self.frequency_knob.setNotchesVisible(True)
        self.frequency_knob.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.frequency_knob.valueChanged.connect(self.on_frequency_change)

        # label for real-time frequency display
        self.freq_label = QLabel(f"{int(self.voice.filter_cutoff)} Hz")
        freq_layout.addWidget(self.freq_label)
        freq_layout.addWidget(self.frequency_knob)
        main_layout.addLayout(freq_layout)

        # initialize knob position
        self.frequency_knob.setValue(int(self.freq_to_dial(self.voice.filter_cutoff)))


        # --- Resonance knob ---
        res_layout = QVBoxLayout()
        res_layout.addWidget(QLabel("Resonance"))
        self.resonance_knob = QDial()
        self.resonance_knob.setMinimum(0)
        self.resonance_knob.setMaximum(100)  # map 0-1 to 0-100
        self.resonance_knob.setValue(int(self.voice.filter_resonance * 100))
        self.resonance_knob.setNotchesVisible(True)
        self.resonance_knob.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.resonance_knob.valueChanged.connect(self.on_resonance_change)
        res_layout.addWidget(self.resonance_knob)
        main_layout.addLayout(res_layout)

        # --- Filter type ---
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Filter Type"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(self.FILTER_TYPES)
        self.type_combo.setCurrentText(self.voice.current_filter_type)
        self.type_combo.currentTextChanged.connect(self.on_type_change)
        type_layout.addWidget(self.type_combo)
        main_layout.addLayout(type_layout)

    # --- Logarithmic mapping functions ---
    def dial_to_freq(self, v, f_min=20.0, f_max=20000.0, v_max=100):
        """Map linear dial [0..v_max] to log frequency [f_min..f_max]"""
        return f_min * (f_max / f_min) ** (v / v_max)

    def freq_to_dial(self, f, f_min=20.0, f_max=20000.0, v_max=100):
        """Map frequency to linear dial value"""
        return int(v_max * math.log(f / f_min) / math.log(f_max / f_min))


    # --- Slot functions ---
    def on_frequency_change(self, value):
        freq = self.dial_to_freq(value)
        self.voice.set_filter_cutoff(freq)
        self.freq_label.setText(f"{int(freq)} Hz")
        self.frequency_knob.setToolTip(f"{int(freq)} Hz")

    def on_resonance_change(self, value):
        self.voice.set_filter_resonance(value / 100.0)

    def on_type_change(self, text):
        self.voice.set_filter_type(text)
