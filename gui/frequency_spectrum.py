from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QTimer
import pyqtgraph as pg
import numpy as np


class FrequencySpectrum(QWidget):
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Plot with black background
        self.plot_widget = pg.PlotWidget(title="Frequency Spectrum")
        self.plot_widget.setBackground('k')
        self.layout.addWidget(self.plot_widget)

        self.plot_widget.setLabel('left', 'Level', units='dB')
        self.plot_widget.setLabel('bottom', 'Frequency', units='Hz')

        # Logarithmic scale for X-axis
        self.plot_widget.setLogMode(x=True, y=False)
        self.plot_widget.setXRange(np.log10(20), np.log10(20000))
        self.plot_widget.setYRange(-80, 0)

        # Bar graph item for spectrum
        self.bar_item = pg.BarGraphItem(
            x=[],
            height=[],
            width=1,
            y0=-80,
            brush=(100, 200, 255, 200)
        )
        self.plot_widget.addItem(self.bar_item)

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_spectrum)
        self.timer.start(50)

        # Custom ticks for frequencies
        axis = self.plot_widget.getAxis('bottom')
        freq_labels = [
            20, 30, 40, 60, 80, 120, 200,
            300, 500, 800, 1000, 2000, 3000,
            4000, 6000, 8000, 12000, 16000, 20000
        ]

        ticks = []
        for f in freq_labels:
            if f >= 1000:
                label = f"{f//1000}k"
            else:
                label = str(f)
            ticks.append((np.log10(f), label))

        axis.setTicks([ticks])

    def update_spectrum(self):
        fft_vals = self.engine.get_fft_magnitude()

        if fft_vals is None or len(fft_vals) < 2:
            # Když není audio, nic nezobrazujeme
            self.bar_item.setOpts(x=[], height=[], width=1)
            return

        # Convert to dB
        db = 20 * np.log10(np.maximum(fft_vals, 1e-10))

        # Frequencies corresponding to FFT bins
        freqs = np.fft.rfftfreq(self.engine.fft_size,
                                1.0 / self.engine.sample_rate)

        # Filter frequencies to the range of human hearing
        mask = (freqs >= 20) & (freqs <= 20000)
        freqs = freqs[mask]
        db = db[mask]

        if len(freqs) == 0:
            self.bar_item.setOpts(x=[], height=[], width=1)
            return

        # Bars at logarithmically spaced frequencies
        num_bars = 100
        log_freqs = np.logspace(np.log10(20), np.log10(20000), num_bars)
        heights = []

        for freq in log_freqs:
            # Find the closest FFT bin for this frequency
            idx = np.argmin(np.abs(freqs - freq))
            heights.append(db[idx])

        heights = np.array(heights)

        # Value threshold for display (e.g., -75 dB)
        threshold = -75
        valid_mask = heights > threshold

        if not np.any(valid_mask):
            # No valid bars to display
            self.bar_item.setOpts(x=[], height=[], width=1)
            return

        # Filter out bars below the threshold
        heights = heights[valid_mask]
        log_freqs_filtered = log_freqs[valid_mask]

        # For log scale, x values are log10 of frequencies
        x_vals = np.log10(log_freqs_filtered)

        # Šířka baru v log prostoru
        if len(x_vals) > 1:
            widths = np.diff(x_vals) * 0.8
            widths = np.append(widths, widths[-1])
        else:
            widths = [0.1]

        self.bar_item.setOpts(
            x=x_vals,
            # Heights are relative to the threshold, so we shift them up by 80 dB
            height=heights - (-80),
            width=np.array(widths),
            y0=-80,  # Lower bound of the bars
            brush=(100, 200, 255, 200)
        )
