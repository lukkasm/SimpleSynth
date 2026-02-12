from signalflow import ADSREnvelope


class ADSR():
    """Simple ADSR envelope generator"""

    def __init__(self,
                 attack=0.01,
                 decay=0.1,
                 sustain=0.8,
                 release=0.2):

        self.attack = attack
        self.decay = decay
        self.sustain = sustain
        self.release = release

        self.node = ADSREnvelope(
            attack=self.attack,
            decay=self.decay,
            sustain=self.sustain,
            release=self.release
        )

    # --- GATE ---
    def gate_on(self):
        self.node.gate = 1

    def gate_off(self):
        self.node.gate = 0

    # --- PARAM UPDATE ---
    def set_attack(self, value):
        self.attack = value
        self.node.attack = value

    def set_decay(self, value):
        self.decay = value
        self.node.decay = value

    def set_sustain(self, value):
        self.sustain = value
        self.node.sustain = value

    def set_release(self, value):
        self.release = value
        self.node.release = value
