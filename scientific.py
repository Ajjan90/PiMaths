from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLabel
import qtawesome as qta

class ScientificCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.display = QtWidgets.QLineEdit()
        layout.addWidget(self.display)

        # Your scientific calculator HisBtns go here
        layout.addWidget(QtWidgets.QPushButton("Scientific Calculator"))