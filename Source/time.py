from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
from pint import UnitRegistry

from Source.timeWidgets.timecon import TimeConversion
from Source.timeWidgets.timeMath import TimeAS
from Source.timeWidgets.timeDiff import DiffernceTime

class TimeCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.converting = False
        self.currentInput = None

        self.setMinimumWidth(380)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # Title
        title = QtWidgets.QLabel("Time Calculation")
        titleFont = QtGui.QFont("Arial", 14)
        titleFont.setBold(True)
        title.setFont(titleFont)

        TimeConvert = TimeConversion()
        TimeasCal = TimeAS(self)
        TimeDiff = DiffernceTime()

        tabControl = QtWidgets.QTabWidget()
        tabControl.addTab(TimeConvert, qta.icon("mdi.alarm-multiple"), "Time Conversion")
        tabControl.addTab(TimeasCal, qta.icon("mdi6.clock-plus-outline"), "Time Add/Subtract")
        tabControl.addTab(TimeDiff, qta.icon("mdi6.clock-start"), "Time Difference")
        tabControl.setStyleSheet("""
                                    QTabBar::tab {
                                        min-height: 42px;
                                        max-height: 42px;
                                    }
                                """)

        mainLayout.addWidget(title)
        mainLayout.addWidget(tabControl)

