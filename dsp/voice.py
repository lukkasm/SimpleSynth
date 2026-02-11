from signalflow import SineOscillator, ADSREnvelope, Constant, ChannelMixer


class Voice:
    def __init__(self):
        self.amp = Constant(0.1)

        # ADSR
        self.env = ADSREnvelope(
            attack=0.01,
            decay=0.1,
            sustain=0.8,
            release=0.2
        )

        # OSC
        self.osc = SineOscillator(440)

        # Mono signal
        mono = self.osc * self.env * self.amp

        # Stereo
        self.stereo = ChannelMixer(2, mono)

        # OUTPUT
        self.output = self.stereo
        self.active = False

    def note_on(self, freq):
        self.osc.frequency = freq
        self.env.gate = 1
        self.active = True

    def note_off(self):
        self.env.gate = 0
        self.active = False
