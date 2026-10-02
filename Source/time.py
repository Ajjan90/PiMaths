from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import qtawesome as qta
from datetime import date
from dateutil.relativedelta import relativedelta

class TimeCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(380)

        MainLayout = QtWidgets.QVBoxLayout(self)
        MainLayout.setContentsMargins(10, 10, 10, 10)

        # Fonts
        self.dateFont = QtGui.QFont("Arial", 16) # Font type for the datetimepicker
        self.lblFont = QtGui.QFont("Arial", 12) # Font type for the labels

        self.headFont = QtGui.QFont("Arial", 13) # Font type for the header labels
        self.headFont.setBold(True) 

        # Title
        self.Lbl = QtWidgets.QLabel("Time Calculation")
        self.titleFont = QtGui.QFont("Arial", 14)
        self.titleFont.setBold(True)
        self.Lbl.setFont(self.titleFont)

        # Tab control
        self.tabControl = QtWidgets.QTabWidget()

        self.TimeConversionTab()

        self.tabControl.addTab(self.timeTab, qta.icon("mdi6.alarm-multiple"), "Time conversion")

        MainLayout.addWidget(self.Lbl)
        MainLayout.addWidget(self.tabControl)


    def TimeConversionTab(self):
        self.timeTab = QtWidgets.QWidget()
        self.timeTabLayout = QtWidgets.QVBoxLayout(self.timeTab)

        # Overall margins and spacing
        self.timeTabLayout.setContentsMargins(10, 10, 10, 10)
        self.timeTabLayout.setSpacing(8)

        # Fonts
        inputFont = QtGui.QFont("Arial", 18)
        comboFont = QtGui.QFont("Arial", 13)

        # -------------------------
        # Top row
        # -------------------------
        self.TopRow = QtWidgets.QHBoxLayout()
        self.TopRow.setContentsMargins(0, 0, 0, 0)

        self.refBtn = QtWidgets.QPushButton()
        self.refBtn.setIcon(qta.icon("msc.debug-restart"))
        self.refBtn.setToolTip("Refresh (Ctrl+R)")
        self.refBtn.setFixedSize(35, 35)

        # Shortcut for refresh
        self.refShtcut = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+R"),
            self.timeTab
        )
        # self.refShtcut.activated.connect(self.refBtn.click)

        self.TopRow.addStretch()
        self.TopRow.addWidget(self.refBtn)

        self.timeTabLayout.addLayout(self.TopRow)

        # -------------------------
        # Validator
        # -------------------------
        validator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(r"\d*\.?\d*")
        )

        # -------------------------
        # First input
        # -------------------------
        self.inputbox1 = QtWidgets.QLineEdit("1")
        self.inputbox1.setFixedHeight(55)
        self.inputbox1.setFont(inputFont)
        self.inputbox1.setValidator(validator)
        #self.inputbox1.textChanged.connect(self.input1Changed)
        self.inputbox1.installEventFilter(self)

        self.timeTabLayout.addWidget(self.inputbox1)

        # -------------------------
        # First unit
        # -------------------------
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFont(comboFont)
        self.combo1.setFixedHeight(40)
        #self.combo1.currentTextChanged.connect(self.unit1Changed)

        self.timeTabLayout.addWidget(self.combo1)

        # -------------------------
        # Swap button
        # -------------------------
        swapRow = QtWidgets.QHBoxLayout()
        swapRow.setContentsMargins(0, 2, 0, 2)

        swapRow.addStretch()

        self.swapButton = QtWidgets.QPushButton()
        self.swapButton.setFixedSize(35, 35)
        self.swapButton.setIcon(qta.icon("fa5s.exchange-alt"))
        self.swapButton.setIconSize(QtCore.QSize(15, 15))
        self.swapButton.setToolTip("Swap units (Ctrl+U)")
        #self.swapButton.clicked.connect(self.swapUnits)

        swapRow.addWidget(self.swapButton)
        swapRow.addStretch()

        self.timeTabLayout.addLayout(swapRow)

        # Shortcut for swap
        swapShortcut = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+U"),
            self.timeTab
        )
        #swapShortcut.activated.connect(self.swapUnits)

        # -------------------------
        # Second input
        # -------------------------
        self.inputbox2 = QtWidgets.QLineEdit("0")
        self.inputbox2.setFixedHeight(55)
        self.inputbox2.setFont(inputFont)
        self.inputbox2.setValidator(validator)
        #self.inputbox2.textChanged.connect(self.input2Changed)
        self.inputbox2.installEventFilter(self)

        self.timeTabLayout.addWidget(self.inputbox2)

        # -------------------------
        # Second unit
        # -------------------------
        self.combo2 = QtWidgets.QComboBox()
        self.combo2.setFont(comboFont)
        self.combo2.setFixedHeight(40)
        self.combo2.setCurrentText("Fahrenheit")
        #self.combo2.currentTextChanged.connect(self.unit2Changed)

        self.timeTabLayout.addWidget(self.combo2)

        # -------------------------
        # Unit comparison label
        # -------------------------
        self.unitLbl = QtWidgets.QLabel()
        self.unitLbl.setFont(QtGui.QFont("Arial", 12))
        self.unitLbl.setStyleSheet("color: gray;")
        self.unitLbl.setAlignment(QtCore.Qt.AlignCenter)

        self.timeTabLayout.addSpacing(8)
        self.timeTabLayout.addWidget(self.unitLbl)

        # Push everything toward the top while keeping
        # consistent spacing between controls.
        self.timeTabLayout.addStretch()