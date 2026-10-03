from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta

from Window.ClockDialog import DigitalClockDialog

class DiffernceTime(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.lblFont = QtGui.QFont("Arial", 12)
        self.dateFont = QtGui.QFont("Arial", 16)
        self.headFont = QtGui.QFont("Arial", 16)

        self.betTimeLayout = QtWidgets.QVBoxLayout(self)
        self.betTimeLayout.setContentsMargins(10, 10, 10, 10)

        self.TopRow = QtWidgets.QHBoxLayout()

        self.refBtn = QtWidgets.QPushButton()
        self.refBtn.setIcon(qta.icon("msc.debug-restart"))
        self.refBtn.setToolTip("Refresh (Ctrl+R)")
        self.refBtn.setFixedSize(35, 35)
        self.refBtn.clicked.connect(self.refreshInputs)

        self.refShortcut = QtGui.QShortcut(
            QtGui.QKeySequence("Ctrl+R"),
            self
        )
        self.refShortcut.activated.connect(self.refBtn.click)

        self.TopRow.addStretch()
        self.TopRow.addWidget(self.refBtn)

        self.strLbl = QtWidgets.QLabel("Start Time")
        self.strLbl.setFont(self.lblFont)

        self.strPicker = QtWidgets.QTimeEdit()
        self.strPicker.setFont(self.dateFont)
        self.strPicker.setTime(QtCore.QTime.currentTime())
        self.strPicker.setDisplayFormat("HH : mm : ss")
        self.strPicker.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.strPicker.timeChanged.connect(self.calculateTime)

        self.strClockBtn = QtWidgets.QPushButton()
        self.strClockBtn.setIcon(qta.icon("fa5s.clock"))
        self.strClockBtn.setToolTip("Select start time")
        self.strClockBtn.setFixedSize(45, 45)
        self.strClockBtn.clicked.connect(self.openStartClock)

        self.strTimeLayout = QtWidgets.QHBoxLayout()
        self.strTimeLayout.setSpacing(6)
        self.strTimeLayout.addWidget(self.strPicker)
        self.strTimeLayout.addWidget(self.strClockBtn)

        self.endLbl = QtWidgets.QLabel("End Time")
        self.endLbl.setFont(self.lblFont)

        self.endPicker = QtWidgets.QTimeEdit()
        self.endPicker.setFont(self.dateFont)
        self.endPicker.setTime(QtCore.QTime.currentTime())
        self.endPicker.setDisplayFormat("HH : mm : ss")
        self.endPicker.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Fixed
        )
        self.endPicker.timeChanged.connect(self.calculateTime)

        self.endClockBtn = QtWidgets.QPushButton()
        self.endClockBtn.setIcon(qta.icon("fa5s.clock"))
        self.endClockBtn.setToolTip("Select end time")
        self.endClockBtn.setFixedSize(45, 45)
        self.endClockBtn.clicked.connect(self.openEndClock)

        self.endTimeLayout = QtWidgets.QHBoxLayout()
        self.endTimeLayout.setSpacing(6)
        self.endTimeLayout.addWidget(self.endPicker)
        self.endTimeLayout.addWidget(self.endClockBtn)

        self.diffHeader = QtWidgets.QLabel("Difference")
        self.diffHeader.setFont(self.headFont)

        self.daysLbl = QtWidgets.QLabel("Same Time")
        self.daysLbl.setFont(self.lblFont)

        self.detLbl = QtWidgets.QLabel("")
        self.detLbl.setFont(self.lblFont)
        self.detLbl.setStyleSheet("color: gray;")

        self.betTimeLayout.addLayout(self.TopRow)

        self.betTimeLayout.addWidget(self.strLbl)
        self.betTimeLayout.addLayout(self.strTimeLayout)

        self.betTimeLayout.addSpacing(35)

        self.betTimeLayout.addWidget(self.endLbl)
        self.betTimeLayout.addLayout(self.endTimeLayout)

        self.betTimeLayout.addSpacing(25)

        self.betTimeLayout.addWidget(self.diffHeader)
        self.betTimeLayout.addWidget(self.daysLbl)
        self.betTimeLayout.addWidget(self.detLbl)

        self.betTimeLayout.addStretch()

        self.calculateTime()

    def openStartClock(self):
        dialog = DigitalClockDialog(
            self.strPicker.time(),
            self
        )

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.strPicker.setTime(dialog.getTime())

    def openEndClock(self):
        dialog = DigitalClockDialog(
            self.endPicker.time(),
            self
        )

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.endPicker.setTime(dialog.getTime())

    def calculateTime(self):
        start = self.strPicker.time()
        end = self.endPicker.time()

        startSeconds = start.hour() * 3600 + start.minute() * 60 + start.second()
        endSeconds = end.hour() * 3600 + end.minute() * 60 + end.second()

        difference = endSeconds - startSeconds

        if difference < 0:
            difference += 24 * 60 * 60

        hours = difference // 3600
        remainingSeconds = difference % 3600
        minutes = remainingSeconds // 60
        seconds = remainingSeconds % 60

        if difference == 0:
            self.daysLbl.setText("Same time")
            self.detLbl.setText("")
        else:
            self.daysLbl.setText(
                f"{hours} hours, {minutes} minutes and {seconds} seconds"
            )

            self.detLbl.setText(
                f"{hours:02d} : {minutes:02d} : {seconds:02d}"
            )

    def refreshInputs(self):
        currentTime = QtCore.QTime.currentTime()

        self.strPicker.setTime(currentTime)
        self.endPicker.setTime(currentTime)

        self.daysLbl.setText("Same time")
        self.detLbl.setText("")
