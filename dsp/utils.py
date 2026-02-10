def midi_to_freq(note: int) -> float:
    return 440.0 * (2 ** ((note - 69) / 12))
