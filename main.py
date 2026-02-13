import ctypes
import sys

from PyQt6.QtWidgets import QApplication

from dsp.engine import AudioEngine
from gui.main_window import MainWindow


ctypes.OleDLL('ole32').CoInitializeEx(0, 2)


engine = AudioEngine()


app = QApplication(sys.argv)
window = MainWindow(engine)
window.show() 
window.setFocus()

sys.exit(app.exec())
