class Tuner:
    """
    Handles musical tuning in semitones relative to a base frequency.
    """

    def __init__(self, base_freq=440.0):
        self.base_freq = base_freq  # default A4
        self.semitone_offset = 0    # semitones

    def set_semitone_offset(self, semitones: int):
        self.semitone_offset = semitones

    def get_frequency(self):
        """
        Returns the frequency in Hz corresponding to current semitone offset.
        """
        return self.base_freq * (2 ** (self.semitone_offset / 12))

    def get_frequency_for_midi(self, midi_note: int):
        """
        Returns the frequency in Hz for a given MIDI note number,
        applying the current semitone offset.
        """
        # Standard A4 = MIDI 69
        semitones_from_a4 = midi_note - 69 + self.semitone_offset
        freq = 440.0 * (2 ** (semitones_from_a4 / 12))
        return freq
