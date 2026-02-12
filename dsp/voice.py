from signalflow import (
    SineOscillator, SawOscillator, SquareOscillator, TriangleOscillator,
    ChannelArray, Constant
)

from dsp.voice_tune import Tuner
from dsp.adsr import ADSR


class Voice:
    def __init__(self):
        self.env = ADSR()
        self.amp = Constant(0.1)

        self.tuner = Tuner(base_freq=440.0)
        self.current_midi_note = 69

        self.active = False
        self.is_playing = False

        # all oscillator types pre-initialized for realtime switching
        self.osc_sine = SineOscillator(self.tuner.get_frequency())
        self.osc_saw = SawOscillator(self.tuner.get_frequency())
        self.osc_square = SquareOscillator(self.tuner.get_frequency())
        self.osc_triangle = TriangleOscillator(self.tuner.get_frequency())

        # realtime safe mix control
        self.sel_sine = Constant(1.0)   # sine default
        self.sel_saw = Constant(0.0)
        self.sel_square = Constant(0.0)
        self.sel_triangle = Constant(0.0)

        # oscillator mix
        mono = (
            self.osc_sine * self.sel_sine +
            self.osc_saw * self.sel_saw +
            self.osc_square * self.sel_square +
            self.osc_triangle * self.sel_triangle
        ) * self.env.node * self.amp

        # stereo output
        self.stereo = ChannelArray([mono, mono])
        self.output = self.stereo

    def start_playing(self):
        if not self.is_playing:
            self.output.play()
            self.is_playing = True

    def note_on(self, midi_note):
        self.current_midi_note = midi_note
        freq = self.tuner.get_frequency_for_midi(midi_note)
        
        self.osc_sine.frequency = freq
        self.osc_saw.frequency = freq
        self.osc_square.frequency = freq
        self.osc_triangle.frequency = freq
        
        self.env.gate_on()
        self.active = True

    def note_off(self):
        self.env.gate_off()
        self.active = False

    def set_oscillator(self, osc_type: str):
        """Thread-safe realtime switch of oscillator"""
        self.sel_sine.set_value(1.0 if osc_type == "sine" else 0.0)
        self.sel_saw.set_value(1.0 if osc_type == "saw" else 0.0)
        self.sel_square.set_value(1.0 if osc_type == "square" else 0.0)
        self.sel_triangle.set_value(1.0 if osc_type == "triangle" else 0.0)

    def update_frequency(self):
        """Call this after tuner changes to update all oscillator frequencies"""
        if self.active:  # pokud držíme notu
            new_freq = self.tuner.get_frequency_for_midi(self.current_midi_note)
            self.osc_sine.frequency = new_freq
            self.osc_saw.frequency = new_freq
            self.osc_square.frequency = new_freq
            self.osc_triangle.frequency = new_freq
