from PySide6 import QtGui, QtWidgets, QtCore
import qtawesome as qta

class DateCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumWidth(380)

        