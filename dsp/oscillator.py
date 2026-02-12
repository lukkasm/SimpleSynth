from signalflow import (
    SineOscillator, SawOscillator,
    SquareOscillator, TriangleOscillator,
    Constant
)

from dsp.voice_tune import Tuner
from dsp.adsr import ADSR


class OscillatorLayer:
    def __init__(self, base_freq=440.0, gain=0.5):

        # tuning
        self.tuner = Tuner(base_freq=base_freq)

        # envelope + amp
        self.env = ADSR()
        self.amp = Constant(gain)

        # oscillators
        freq = self.tuner.get_frequency()

        self.osc_sine = SineOscillator(freq)
        self.osc_saw = SawOscillator(freq)
        self.osc_square = SquareOscillator(freq)
        self.osc_triangle = TriangleOscillator(freq)

        # waveform selector
        self.sel_sine = Constant(1.0)
        self.sel_saw = Constant(0.0)
        self.sel_square = Constant(0.0)
        self.sel_triangle = Constant(0.0)

        # oscillator mix
        osc_mix = (
            self.osc_sine * self.sel_sine +
            self.osc_saw * self.sel_saw +
            self.osc_square * self.sel_square +
            self.osc_triangle * self.sel_triangle
        ) * self.env.node * self.amp

        # stereo output
        self.output = osc_mix * self.env.node * self.amp

    # -------------------------

    def set_oscillator(self, osc_type: str):
        self.sel_sine.set_value(1.0 if osc_type == "sine" else 0.0)
        self.sel_saw.set_value(1.0 if osc_type == "saw" else 0.0)
        self.sel_square.set_value(1.0 if osc_type == "square" else 0.0)
        self.sel_triangle.set_value(1.0 if osc_type == "triangle" else 0.0)

    def set_gain(self, value: float):
        self.amp.set_value(value)

    def set_frequency_from_midi(self, midi_note: int):
        self.current_midi_note = midi_note
        freq = self.tuner.get_frequency_for_midi(midi_note)
        self._set_frequency(freq)

    def update_frequency(self):
        freq = self.tuner.get_frequency_for_midi(self.current_midi_note)
        self._set_frequency(freq)

    def gate_on(self):
        self.env.gate_on()

    def gate_off(self):
        self.env.gate_off()

    # ---------------------------------------------------------

    def _set_frequency(self, freq):
        self.osc_sine.frequency = freq
        self.osc_saw.frequency = freq
        self.osc_square.frequency = freq
        self.osc_triangle.frequency = freq
