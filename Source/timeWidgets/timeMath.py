from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from Window.ClockDialog import DigitalClockDialog

class TimeAS(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.lblFont = QtGui.QFont("Arial", 12)
        self.timeFont = QtGui.QFont("Arial", 16)

        self.asTimeLayout = QtWidgets.QVBoxLayout(self)
        self.asTimeLayout.setContentsMargins(10, 10, 10, 10)
        self.asTimeLayout.setSpacing(12)

        # Refresh button
        self.refBtn = QtWidgets.QPushButton()
        self.refBtn.setIcon(qta.icon("msc.debug-restart"))
        self.refBtn.setToolTip("Refresh (Ctrl+R)")
        self.refBtn.setFixedSize(35, 35)
        self.refBtn.clicked.connect(self.refreshInputs)

        self.refShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self)
        self.refShortcut.activated.connect(self.refreshInputs)

        # Add / Subtract
        self.radioLayout = QtWidgets.QHBoxLayout()
        self.radioLayout.setSpacing(20)

        self.addRadio = QtWidgets.QRadioButton("Add (+)")
        self.addRadio.setFont(self.lblFont)
        self.addRadio.setChecked(True)
        self.addRadio.toggled.connect(self.timeCalculation)

        self.subRadio = QtWidgets.QRadioButton("Subtract (-)")
        self.subRadio.setFont(self.lblFont)
        self.subRadio.toggled.connect(self.timeCalculation)

        self.radioLayout.addWidget(self.addRadio)
        self.radioLayout.addWidget(self.subRadio)
        self.radioLayout.addStretch()
        self.radioLayout.addWidget(self.refBtn)

        # Time label
        self.fromLbl = QtWidgets.QLabel("Time")
        self.fromLbl.setFont(self.lblFont)

        # Time input and clock button
        self.timeInputLayout = QtWidgets.QHBoxLayout()
        self.timeInputLayout.setSpacing(6)

        self.fromPicker = QtWidgets.QTimeEdit()
        self.fromPicker.setFont(self.timeFont)
        self.fromPicker.setTime(QtCore.QTime.currentTime())
        self.fromPicker.setDisplayFormat("HH : mm : ss")
        self.fromPicker.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.fromPicker.timeChanged.connect(self.timeCalculation)

        self.clockButton = QtWidgets.QPushButton()
        self.clockButton.setIcon(qta.icon("fa5s.clock"))
        self.clockButton.setToolTip("Open digital clock")
        self.clockButton.setFixedSize(45, 45)
        self.clockButton.clicked.connect(self.openClockDialog)

        self.timeInputLayout.addWidget(self.fromPicker)
        self.timeInputLayout.addWidget(self.clockButton)

        # Hours, minutes and seconds
        self.numGroup = QtWidgets.QGroupBox("Hours, Minutes and Seconds")
        self.numGroup.setFont(self.lblFont)

        self.numLayout = QtWidgets.QHBoxLayout(self.numGroup)
        self.numLayout.setContentsMargins(10, 10, 10, 10)
        self.numLayout.setSpacing(10)

        # Hours
        self.hourLayout = QtWidgets.QVBoxLayout()

        self.hourLbl = QtWidgets.QLabel("Hours")
        self.hourLbl.setFont(self.lblFont)

        self.hourNum = QtWidgets.QSpinBox()
        self.hourNum.setFont(self.timeFont)
        self.hourNum.setRange(0, 999999)
        self.hourNum.valueChanged.connect(self.timeCalculation)

        self.hourLayout.addWidget(self.hourLbl)
        self.hourLayout.addWidget(self.hourNum)

        # Minutes
        self.minuteLayout = QtWidgets.QVBoxLayout()

        self.minuteLbl = QtWidgets.QLabel("Minutes")
        self.minuteLbl.setFont(self.lblFont)

        self.minuteNum = QtWidgets.QSpinBox()
        self.minuteNum.setFont(self.timeFont)
        self.minuteNum.setRange(0, 999999)
        self.minuteNum.valueChanged.connect(self.timeCalculation)

        self.minuteLayout.addWidget(self.minuteLbl)
        self.minuteLayout.addWidget(self.minuteNum)

        # Seconds
        self.secondLayout = QtWidgets.QVBoxLayout()

        self.secondLbl = QtWidgets.QLabel("Seconds")
        self.secondLbl.setFont(self.lblFont)

        self.secondNum = QtWidgets.QSpinBox()
        self.secondNum.setFont(self.timeFont)
        self.secondNum.setRange(0, 999999)
        self.secondNum.valueChanged.connect(self.timeCalculation)

        self.secondLayout.addWidget(self.secondLbl)
        self.secondLayout.addWidget(self.secondNum)

        self.numLayout.addLayout(self.hourLayout)
        self.numLayout.addLayout(self.minuteLayout)
        self.numLayout.addLayout(self.secondLayout)

        # Output
        self.outlbl = QtWidgets.QLabel()
        self.outlbl.setFont(self.lblFont)

        self.asTimeLayout.addLayout(self.radioLayout)
        self.asTimeLayout.addSpacing(10)
        self.asTimeLayout.addWidget(self.fromLbl)
        self.asTimeLayout.addLayout(self.timeInputLayout)
        self.asTimeLayout.addSpacing(15)
        self.asTimeLayout.addWidget(self.numGroup)
        self.asTimeLayout.addSpacing(15)
        self.asTimeLayout.addWidget(self.outlbl)
        self.asTimeLayout.addStretch()

        self.timeCalculation()

    def openClockDialog(self):
        dialog = DigitalClockDialog(self.fromPicker.time(), self)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.fromPicker.setTime(dialog.getTime())

    def timeCalculation(self):
        fromTime = self.fromPicker.time()

        hours = self.hourNum.value()
        minutes = self.minuteNum.value()
        seconds = self.secondNum.value()

        totalSeconds = (hours * 3600) + (minutes * 60) + seconds

        if self.addRadio.isChecked():
            resultTime = fromTime.addSecs(totalSeconds)
        else:
            resultTime = fromTime.addSecs(-totalSeconds)

        self.outlbl.setText(f"Time: {resultTime.toString('HH : mm : ss')}")

    def refreshInputs(self):
        self.fromPicker.setTime(QtCore.QTime.currentTime())
        self.hourNum.setValue(0)
        self.minuteNum.setValue(0)
        self.secondNum.setValue(0)
        self.addRadio.setChecked(True)
        self.timeCalculation()