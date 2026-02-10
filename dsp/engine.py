from signalflow import *
from dsp.voice import Voice
from dsp.utils import midi_to_freq


class AudioEngine:
    def __init__(self):
        self.graph = AudioGraph()

        # Stereo
        self.voice = Voice()
        self.voice.output.play()

    def note_on(self, note: int):
        freq = midi_to_freq(note)
        self.voice.note_on(freq)

    def note_off(self):
        self.voice.note_off()
