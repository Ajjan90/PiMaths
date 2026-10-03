from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta


class DigitalClockDialog(QtWidgets.QDialog):
    def __init__(self, selectedTime, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Select Time")
        self.setModal(True)
        self.setFixedSize(420, 420)

        self.selectedTime = selectedTime

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        titleLbl = QtWidgets.QLabel("Select Time")
        titleLbl.setFont(QtGui.QFont("Arial", 16))
        titleLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(titleLbl)

        self.timeDisplay = QtWidgets.QTimeEdit()
        self.timeDisplay.setTime(selectedTime)
        self.timeDisplay.setDisplayFormat("HH : mm : ss")
        self.timeDisplay.setFont(QtGui.QFont("Arial", 22))
        self.timeDisplay.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.timeDisplay.setReadOnly(True)

        layout.addWidget(self.timeDisplay)

        dialLayout = QtWidgets.QHBoxLayout()
        dialLayout.setSpacing(30)

        hourLayout = QtWidgets.QVBoxLayout()
        hourLayout.setSpacing(5)

        hourTitle = QtWidgets.QLabel("Hours")
        hourTitle.setFont(QtGui.QFont("Arial", 12))
        hourTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.hourDial = QtWidgets.QDial()
        self.hourDial.setRange(0, 23)
        self.hourDial.setValue(selectedTime.hour())
        self.hourDial.setWrapping(True)
        self.hourDial.setNotchesVisible(True)
        self.hourDial.setNotchTarget(30)
        self.hourDial.setFixedSize(120, 120)

        self.hourValue = QtWidgets.QLabel()
        self.hourValue.setFont(QtGui.QFont("Arial", 14))
        self.hourValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.hourValue.setText(f"{selectedTime.hour():02d}")

        hourLayout.addWidget(hourTitle)
        hourLayout.addWidget(self.hourDial, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        hourLayout.addWidget(self.hourValue)

        minuteLayout = QtWidgets.QVBoxLayout()
        minuteLayout.setSpacing(5)

        minuteTitle = QtWidgets.QLabel("Minutes")
        minuteTitle.setFont(QtGui.QFont("Arial", 12))
        minuteTitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.minuteDial = QtWidgets.QDial()
        self.minuteDial.setRange(0, 59)
        self.minuteDial.setValue(selectedTime.minute())
        self.minuteDial.setWrapping(True)
        self.minuteDial.setNotchesVisible(True)
        self.minuteDial.setNotchTarget(30)
        self.minuteDial.setFixedSize(120, 120)

        self.minuteValue = QtWidgets.QLabel()
        self.minuteValue.setFont(QtGui.QFont("Arial", 14))
        self.minuteValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.minuteValue.setText(f"{selectedTime.minute():02d}")

        minuteLayout.addWidget(minuteTitle)
        minuteLayout.addWidget(self.minuteDial, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        minuteLayout.addWidget(self.minuteValue)

        dialLayout.addLayout(hourLayout)
        dialLayout.addLayout(minuteLayout)

        layout.addLayout(dialLayout)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.setSpacing(10)

        self.cancelButton = QtWidgets.QPushButton("Cancel")
        self.cancelButton.setMinimumHeight(40)
        self.cancelButton.clicked.connect(self.reject)

        self.setButton = QtWidgets.QPushButton("Set Time")
        self.setButton.setMinimumHeight(40)
        self.setButton.clicked.connect(self.accept)

        buttonLayout.addWidget(self.cancelButton)
        buttonLayout.addWidget(self.setButton)

        layout.addLayout(buttonLayout)

        self.hourDial.valueChanged.connect(self.updateTime)
        self.minuteDial.valueChanged.connect(self.updateTime)

    def updateTime(self):
        hour = self.hourDial.value()
        minute = self.minuteDial.value()

        self.hourValue.setText(f"{hour:02d}")
        self.minuteValue.setText(f"{minute:02d}")

        current = self.timeDisplay.time()

        newTime = QtCore.QTime(
            hour,
            minute,
            current.second()
        )

        self.timeDisplay.setTime(newTime)
        self.selectedTime = newTime

    def getTime(self):
        return self.selectedTime