import sys
import logging

from PyQt5.QtWidgets import QApplication, QMainWindow

# Create an PyQT4 application object.
from ui.controller import MainUIController

app = QApplication(sys.argv)
window = QMainWindow()

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

controller = MainUIController(window, app)

window.show()
sys.exit(app.exec_())