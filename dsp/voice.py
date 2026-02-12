from signalflow import ChannelArray

from dsp.oscillator import OscillatorLayer


class Voice:
    def __init__(self):
        self.layer1 = OscillatorLayer(gain=0.5)
        self.layer2 = OscillatorLayer(gain=0.5)

        mono = self.layer1.output + self.layer2.output
        
        self.output = ChannelArray([mono, mono])

        self.current_note = None
        self.active = False

    def note_on(self, midi_note: int):

        self.current_note = midi_note

        # nastav frekvence
        self.layer1.set_frequency_from_midi(midi_note)
        self.layer2.set_frequency_from_midi(midi_note)

        # otevři obálky
        self.layer1.gate_on()
        self.layer2.gate_on()

        self.active = True

    def note_off(self):

        self.layer1.gate_off()
        self.layer2.gate_off()

        self.active = False

    def update_frequency(self):
        if self.active and self.current_note is not None:
            self.layer1.update_frequency()
            self.layer2.update_frequency()
