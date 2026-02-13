from signalflow import AudioGraph, ChannelMixer, BufferRecorder, Buffer
import numpy as np

from dsp.voice import Voice


class AudioEngine:
    def __init__(self, fft_size=4096):
        self.graph = AudioGraph()
        self.graph.start()

        # Stereo voice
        self.voice = Voice()
        self.voice.output.play()

        self.sample_rate = self.graph.sample_rate
        self.block_size = 8192

        # Mono buffer for FFT
        self.buffer = Buffer(num_channels=1, num_frames=fft_size * 2)

        # Create a mono signal by mixing the stereo output of the voice
        mono_signal = ChannelMixer(1, self.voice.output)

        self.recorder = BufferRecorder(
            input=mono_signal,
            buffer=self.buffer,
            loop=True
        )
        self.recorder.play()

        self.fft_size = fft_size

    def note_on(self, midi_note: int):
        """Play note with MIDI note number (not frequency)"""
        self.voice.note_on(midi_note)

    def note_off(self):
        self.voice.note_off()

    def get_fft_magnitude(self):
        buf = self.buffer.data

        if buf is None:
            return None

        if buf.ndim > 1:
            buf = buf[0, :]

        print("Max value in buffer:", np.max(buf))

        if len(buf) >= self.fft_size:
            buf = buf[-self.fft_size:]
        else:
            buf = np.pad(buf, (0, self.fft_size - len(buf)))

        window = np.hanning(self.fft_size)
        windowed = buf * window

        fft_vals = np.abs(np.fft.rfft(windowed))
        return fft_vals
