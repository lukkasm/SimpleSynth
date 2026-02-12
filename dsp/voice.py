from signalflow import ChannelArray, Constant, SVFilter

from dsp.oscillator import OscillatorLayer


class Voice:
    def __init__(self):
        self.layer1 = OscillatorLayer(gain=0.5)
        self.layer2 = OscillatorLayer(gain=0.5)

        # Mix oscillator layers
        mixed = self.layer1.output + self.layer2.output

        # Filter parameters
        self.filter_cutoff = 1000.0
        self.filter_resonance = 0.5

        # Create all filter types at once using SVFilter directly
        self.filter_lp = SVFilter(
            input=mixed,
            filter_type="low_pass",
            cutoff=self.filter_cutoff,
            resonance=self.filter_resonance
        )
        self.filter_bp = SVFilter(
            input=mixed,
            filter_type="band_pass",
            cutoff=self.filter_cutoff,
            resonance=self.filter_resonance
        )
        self.filter_hp = SVFilter(
            input=mixed,
            filter_type="high_pass",
            cutoff=self.filter_cutoff,
            resonance=self.filter_resonance
        )
        self.filter_notch = SVFilter(
            input=mixed,
            filter_type="notch",
            cutoff=self.filter_cutoff,
            resonance=self.filter_resonance
        )

        # Gains to select which filter is active (default: low_pass)
        self.gain_lp = Constant(1.0)
        self.gain_bp = Constant(0.0)
        self.gain_hp = Constant(0.0)
        self.gain_notch = Constant(0.0)

        # Mix filters
        filtered = (
            self.filter_lp * self.gain_lp +
            self.filter_bp * self.gain_bp +
            self.filter_hp * self.gain_hp +
            self.filter_notch * self.gain_notch
        )

        # Stereo output
        self.output = ChannelArray([filtered, filtered])

        self.current_note = None
        self.active = False

        # Map for easy access
        self.filter_map = {
            "low_pass": (self.filter_lp, self.gain_lp),
            "band_pass": (self.filter_bp, self.gain_bp),
            "high_pass": (self.filter_hp, self.gain_hp),
            "notch": (self.filter_notch, self.gain_notch),
        }
        self.current_filter_type = "low_pass"

    def set_filter_type(self, filter_type: str):
        """Switch active filter by changing gains"""
        if filter_type not in self.filter_map:
            return

        # Turn off all filters
        for name, (filt, gain) in self.filter_map.items():
            gain.set_value(0.0)

        # Turn on selected filter
        self.filter_map[filter_type][1].set_value(1.0)
        self.current_filter_type = filter_type

    def set_filter_cutoff(self, cutoff: float):
        """Update cutoff for all filters"""
        self.filter_cutoff = cutoff
        for filt, gain in self.filter_map.values():
            filt.set_input("cutoff", cutoff)

    def set_filter_resonance(self, resonance: float):
        """Update resonance for all filters"""
        self.filter_resonance = resonance
        for filt, gain in self.filter_map.values():
            filt.set_input("resonance", resonance)

    def note_on(self, midi_note: int):
        self.current_note = midi_note
        self.layer1.set_frequency_from_midi(midi_note)
        self.layer2.set_frequency_from_midi(midi_note)
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
