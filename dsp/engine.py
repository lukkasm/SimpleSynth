from signalflow import AudioGraph, ChannelMixer, BufferRecorder, Buffer
import numpy as np

from dsp.voice import Voice
from dsp.utils import midi_to_freq


class AudioEngine:
    def __init__(self, fft_size=1024):
        self.graph = AudioGraph()
        self.graph.start()

        # Stereo voice
        self.voice = Voice()
        self.voice.start_playing()

        self.sample_rate = self.graph.sample_rate
        self.block_size = 8192

        # Mono buffer for FFT
        self.buffer = Buffer(num_channels=1, num_frames=fft_size * 2)

        # Add ChannelMixer to convert stereo to mono for recording
        self._update_recorder()

        self.fft_size = fft_size

    def _update_recorder(self):
        """Actualizes the BufferRecorder with the current voice output"""
        # Zastavíme starý recorder, pokud existuje
        if hasattr(self, 'recorder'):
            try:
                self.recorder.stop()
            except:
                pass

        # Create a mono signal by mixing the stereo output of the voice
        mono_signal = ChannelMixer(1, self.voice.output)

        self.recorder = BufferRecorder(
            input=mono_signal,
            buffer=self.buffer,
            loop=True
        )
        self.recorder.play()

    def note_on(self, note: int):
        freq = midi_to_freq(note)
        self.voice.note_on(freq)

    def note_off(self):
        self.voice.note_off()

    def get_fft_magnitude(self):
        buf = self.buffer.data

        if buf is None:
            return None

        if buf.ndim > 1:
            buf = buf[0, :]

        if len(buf) > self.fft_size:
            buf = buf[:self.fft_size]
        elif len(buf) < self.fft_size:
            buf = np.pad(buf, (0, self.fft_size - len(buf)))

        window = np.hanning(self.fft_size)
        windowed = buf * window

        fft_vals = np.abs(np.fft.rfft(windowed))

        if np.max(fft_vals) > 1e-10:
            fft_vals = fft_vals / np.max(fft_vals)
        return fft_vals
