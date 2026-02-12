from PyQt6.QtWidgets import QSlider, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt



class ADSRWidget(QWidget):
    """ADSR envelope parameters"""

    def __init__(self, envelope):
        super().__init__()
        self.env = envelope

        layout = QVBoxLayout()
        self.setLayout(layout)

        # ADSR label
        self.label = QLabel(f"ADSR: " 
                            f"A={envelope.attack:.2f}s "
                            f"D={envelope.decay:.2f}s "
                            f"S={envelope.sustain:.2f} "
                            f"R={envelope.release:.2f}s")
        layout.addWidget(self.label)

        # Attack slider
        self.attack_slider = QSlider(Qt.Orientation.Horizontal)
        self.attack_slider.setRange(0, 5000)  # 0 to
        self.attack_slider.setValue(int(self.env.attack * 1000))
        self.attack_slider.valueChanged.connect(self.on_change)
        layout.addWidget(QLabel("Attack (ms)"))
        layout.addWidget(self.attack_slider)

        # Decay slider
        self.decay_slider = QSlider(Qt.Orientation.Horizontal)
        self.decay_slider.setRange(0, 5000)  # 0 to 5 seconds
        self.decay_slider.setValue(int(self.env.decay * 1000))
        self.decay_slider.valueChanged.connect(self.on_change)
        layout.addWidget(QLabel("Decay (ms)"))
        layout.addWidget(self.decay_slider)

        # Sustain slider
        self.sustain_slider = QSlider(Qt.Orientation.Horizontal)
        self.sustain_slider.setRange(0, 100)  # 0 to
        self.sustain_slider.setValue(int(self.env.sustain * 100))
        self.sustain_slider.valueChanged.connect(self.on_change)
        layout.addWidget(QLabel("Sustain"))
        layout.addWidget(self.sustain_slider)

        # Release slider
        self.release_slider = QSlider(Qt.Orientation.Horizontal)
        self.release_slider.setRange(0, 5000)  # 0 to
        self.release_slider.setValue(int(self.env.release * 1000))
        self.release_slider.valueChanged.connect(self.on_change)
        layout.addWidget(QLabel("Release (ms)"))
        layout.addWidget(self.release_slider)

    def on_change(self, value):
        attack = self.attack_slider.value() / 1000.0
        decay = self.decay_slider.value() / 1000.0
        sustain = self.sustain_slider.value() / 100.0
        release = self.release_slider.value() / 1000.0

        self.env.set_attack(attack)
        self.env.set_decay(decay)
        self.env.set_sustain(sustain)
        self.env.set_release(release)

        self.label.setText(f"ADSR: "
                           f"A={attack:.2f}s "
                           f"D={decay:.2f}s "
                           f"S={sustain:.2f} "
                           f"R={release:.2f}s"
                           )
