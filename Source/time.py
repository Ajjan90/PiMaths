from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
from pint import UnitRegistry

from Source.timeWidgets.timecon import TimeConversion

class TimeCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.converting = False
        self.currentInput = None

        self.setMinimumWidth(380)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # Fonts
        inputFont = QtGui.QFont("Arial", 18)
        comboFont = QtGui.QFont("Arial", 13)
        buttonFont = QtGui.QFont("Arial", 15)

        # Title
        title = QtWidgets.QLabel("Time Calculation")
        titleFont = QtGui.QFont("Arial", 14)
        titleFont.setBold(True)
        title.setFont(titleFont)

        TimeConvert = TimeConversion()

        tabControl = QtWidgets.QTabWidget()
        tabControl.addTab(TimeConvert, qta.icon("mdi.alarm-multiple"), "Time Conversion")
        tabControl.setStyleSheet("""
                                    QTabBar::tab {
                                        min-height: 42px;
                                        max-height: 42px;
                                    }
                                """)

        mainLayout.addWidget(title)
        mainLayout.addWidget(tabControl)

