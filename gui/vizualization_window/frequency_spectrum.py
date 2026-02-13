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

        # Plot
        self.plot_widget = pg.PlotWidget(title="Frequency Spectrum")
        self.plot_widget.setBackground('k')
        self.layout.addWidget(self.plot_widget)
        self.plot_widget.setLabel('left', 'Level', units='dB')
        self.plot_widget.setLabel('bottom', 'Frequency', units='Hz')

        # Logarithmic X-axis
        self.plot_widget.setLogMode(x=True, y=False)
        self.plot_widget.enableAutoRange(x=False, y=False)
        self.plot_widget.setYRange(-120, 0)

        # Curve
        self.curve = self.plot_widget.plot(
            pen=pg.mkPen((100, 200, 255), width=2))

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_spectrum)
        self.timer.start(50)

        # X-axis ticks (logarithmic)
        freq_ticks = [20, 30, 40, 60, 80, 120, 200, 300, 500, 800,
                      1000, 2000, 3000, 4000, 6000, 8000, 12000, 16000, 20000]
        axis = self.plot_widget.getAxis('bottom')
        ticks = [(np.log10(f), str(f) if f <
                  1000 else f"{f//1000}k") for f in freq_ticks]
        axis.setTicks([ticks])

        self.prev_db = None
        self.smoothing = 0.6

    def update_spectrum(self):
        fft_vals = self.engine.get_fft_magnitude()
        if fft_vals is None or len(fft_vals) < 2:
            self.curve.setData([], [])
            return

        # FFT frekvence
        freqs = np.fft.rfftfreq(self.engine.fft_size,
                                1.0 / self.engine.sample_rate)

        # Filtrujeme na slyšitelné frekvence
        mask = (freqs >= 20) & (freqs <= 20000)
        freqs = freqs[mask]
        db = 20 * np.log10(np.maximum(fft_vals[mask], 1e-12))
        db = np.clip(db, -120, 0)

        # Logaritmická interpolace pro husté body
        log_freqs = np.logspace(np.log10(20), np.log10(20000), 1000)
        db_interp = np.interp(np.log10(log_freqs), np.log10(freqs), db)

        # Smoothing mezi snímky
        if self.prev_db is None:
            self.prev_db = db_interp
        else:
            self.prev_db = self.smoothing * self.prev_db + \
                (1 - self.smoothing) * db_interp

        # Posíláme data do grafu v log prostoru
        self.curve.setData(np.log10(log_freqs), self.prev_db)
