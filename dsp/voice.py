from signalflow import SineOscillator, ADSREnvelope, Constant


class Voice:
    def __init__(self):
        self.amp = Constant(0.2)

        # ADSR
        self.env = ADSREnvelope(
            attack=0.01,
            decay=0.1,
            sustain=0.8,
            release=0.2
        )

        # OSC
        self.osc = SineOscillator([440, 440])
        
        # OUTPUT
        self.output = self.osc * self.env * self.amp
        self.active = False

    def note_on(self, freq: float):
        self.osc.frequency = freq
        self.env.gate = 1
        self.active = True

    def note_off(self):
        self.env.gate = 0
        self.active = False
