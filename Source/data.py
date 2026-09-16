from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
from pint import UnitRegistry

# Data units
data_measurements = [
    "Bits",
    "Bytes",
    "Kilobits",
    "Kibibytes",
    "Kilobytes",
    "Mebibytes",
    "Megabits",
    "Megabytes",
    "Gibibytes",
    "Gigabits",
    "Gigabytes",
    "Tebibytes",
    "Terabits",
    "Terabytes",
    "Pebibytes",
    "Petabits",
    "Petabytes",
    "Exbibytes",
    "Exabytes",
    "Zebibytes",
    "Zettabytes",
    "Yobibytes",
    "Yottabytes",
    "Ronnabytes",
    "Quettabytes",
]


class DataCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.u = UnitRegistry()
        self.converting = False
        self.currentInput = None

        self.setMinimumWidth(380)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)

        # Fonts
        inputFont = QtGui.QFont("Arial", 18)
        comboFont = QtGui.QFont("Arial", 13)
        buttonFont = QtGui.QFont("Arial", 15)

        # Title and keypad toggle
        topRow = QtWidgets.QHBoxLayout()

        # Title
        title = QtWidgets.QLabel("Data")
        titleFont = QtGui.QFont("Arial", 14)
        titleFont.setBold(True)
        title.setFont(titleFont)

        self.toggleBtn = QtWidgets.QCheckBox("Show buttons")
        self.toggleBtn.setToolTip("Show buttons (Ctrl+I)")
        self.toggleBtn.toggled.connect(self.showButtons)

        toggleShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+I"), self)
        toggleShortcut.activated.connect(self.toggleBtn.toggle)

        topRow.addWidget(title)
        topRow.addStretch()
        topRow.addWidget(self.toggleBtn)
        mainLayout.addLayout(topRow)

        # Number validator
        validator = QtGui.QRegularExpressionValidator(
            QtCore.QRegularExpression(r"\d*\.?\d*")
        )

        # First input
        self.inputbox1 = QtWidgets.QLineEdit("1")
        self.inputbox1.setFixedHeight(55)
        self.inputbox1.setFont(inputFont)
        self.inputbox1.setValidator(validator)
        self.inputbox1.textChanged.connect(self.input1Changed)
        self.inputbox1.installEventFilter(self)

        # First unit
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFont(comboFont)
        self.combo1.setMinimumHeight(40)
        self.combo1.addItems(data_measurements)
        #self.combo1.setCurrentText("Square Meters")
        self.combo1.currentTextChanged.connect(self.unit1Changed)

        # Swap button
        self.swapButton = QtWidgets.QPushButton()
        self.swapButton.setFixedSize(35, 35)
        self.swapButton.setIcon(qta.icon("fa5s.exchange-alt"))
        self.swapButton.setIconSize(QtCore.QSize(15, 15))
        self.swapButton.setToolTip("Swap units (Ctrl+U)")
        self.swapButton.clicked.connect(self.swapUnits)

        swapShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        swapShortcut.activated.connect(self.swapUnits)

        # Second input
        self.inputbox2 = QtWidgets.QLineEdit("0")
        self.inputbox2.setFixedHeight(55)
        self.inputbox2.setFont(inputFont)
        self.inputbox2.setValidator(validator)
        self.inputbox2.textChanged.connect(self.input2Changed)
        self.inputbox2.installEventFilter(self)

        # Second unit
        self.combo2 = QtWidgets.QComboBox()
        self.combo2.setFont(comboFont)
        self.combo2.setMinimumHeight(40)
        self.combo2.addItems(data_measurements)
        #self.combo2.setCurrentText("Square Feet")
        self.combo2.currentTextChanged.connect(self.unit2Changed)

        # Unit comparison label
        self.unitLbl = QtWidgets.QLabel()
        self.unitLbl.setFont(QtGui.QFont("Arial", 12))
        self.unitLbl.setStyleSheet("color: gray;")

        # Keypad
        self.buttonGridWidget = QtWidgets.QWidget()
        buttonGrid = QtWidgets.QGridLayout(self.buttonGridWidget)
        buttonGrid.setContentsMargins(0, 10, 0, 0)
        buttonGrid.setSpacing(5)

        buttons = [
            ["CE", "backspace"],
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [".", "0"],
        ]

        for row, buttonRow in enumerate(buttons):
            for col, text in enumerate(buttonRow):
                button = QtWidgets.QPushButton()
                button.setFont(buttonFont)
                button.setFixedHeight(50)

                if text == "backspace":
                    button.setIcon(qta.icon("fa5s.backspace"))
                    button.setIconSize(QtCore.QSize(18, 18))
                    button.clicked.connect(
                        lambda _, value=text: self.operation_clicked(value)
                    )
                elif text.isdigit() or text == ".":
                    button.setText(text)
                    button.clicked.connect(
                        lambda _, value=text: self.number_clicked(value)
                    )
                else:
                    button.setText(text)
                    button.clicked.connect(
                        lambda _, value=text: self.operation_clicked(value)
                    )

                buttonGrid.addWidget(button, row, col)

        self.buttonGridWidget.setVisible(False)

        # Build the layout
        mainLayout.addWidget(self.inputbox1)
        mainLayout.addWidget(self.combo1)

        swapLayout = QtWidgets.QHBoxLayout()
        swapLayout.addStretch()
        swapLayout.addWidget(self.swapButton)
        swapLayout.addStretch()
        mainLayout.addLayout(swapLayout)

        mainLayout.addWidget(self.inputbox2)
        mainLayout.addWidget(self.combo2)
        mainLayout.addWidget(self.unitLbl)
        mainLayout.addWidget(self.buttonGridWidget)

        #self.convertFirst()
        self.updateUnitLabel()

    # Convert a unit name into a Pint unit.
    def PintUnit(self, unit_name):
        units = {
            "Bits": self.u.bit,
            "Bytes": self.u.byte,
            "Kilobits": self.u.kilobit,
            "Kibibytes": self.u.kibibyte,
            "Kilobytes": self.u.kilobyte,
            "Mebibytes": self.u.mebibyte,
            "Megabits": self.u.megabit,
            "Megabytes": self.u.megabyte,
            "Gibibytes": self.u.gibibyte,
            "Gigabits": self.u.gigabit,
            "Gigabytes": self.u.gigabyte,
            "Tebibytes": self.u.tebibyte,
            "Terabits": self.u.terabit,
            "Terabytes": self.u.terabyte,
            "Pebibytes": self.u.pebibyte,
            "Petabits": self.u.petabit,
            "Petabytes": self.u.petabyte,
            "Exbibytes": self.u.exbibyte,
            "Exabytes": self.u.exabyte,
            "Zebibytes": self.u.zebibyte,
            "Zettabytes": self.u.zettabyte,
            "Yobibytes": self.u.yobibyte,
            "Yottabytes": self.u.yottabyte,
            "Ronnabytes": self.u.ronnabyte,
            "Quettabytes": self.u.quettabyte,
        }
        return units[unit_name]


    # Return the short display name for a unit.
    def unitDisplayName(self, unit_name):
        names = {
            "Bits": "bit",
            "Bytes": "B",
            "Kilobits": "Kbit",
            "Kibibytes": "KiB",
            "Kilobytes": "KB",
            "Mebibytes": "MiB",
            "Megabits": "Mbit",
            "Megabytes": "MB",
            "Gibibytes": "GiB",
            "Gigabits": "Gbit",
            "Gigabytes": "GB",
            "Tebibytes": "TiB",
            "Terabits": "Tbit",
            "Terabytes": "TB",
            "Petabits": "Pbit",
            "Petabytes": "PB",
            "Exbibytes": "EiB",
            "Exabytes": "EB",
            "Zebibytes": "ZiB",
            "Zettabytes": "ZB",
            "Yobibytes": "YiB",
            "Yottabytes": "YB",
            "Ronnabytes": "RB",
            "Quettabytes": "QB",
        }
        return names[unit_name]

    # Track which input currently has focus.
    def focusInEvent(self, event):
        super().focusInEvent(event)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.FocusIn:
            if obj in (self.inputbox1, self.inputbox2):
                self.currentInput = obj

        if event.type() != QtCore.QEvent.Type.KeyPress:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QtWidgets.QLineEdit):
            return super().eventFilter(obj, event)

        modifiers = event.modifiers()

        if modifiers & (
            QtCore.Qt.KeyboardModifier.ControlModifier
            | QtCore.Qt.KeyboardModifier.AltModifier
        ):
            return super().eventFilter(obj, event)

        key = event.key()
        text = event.text()

        self.currentInput = obj

        if text.isdigit():
            self.number_clicked(text)
            return True

        if text == ".":
            self.number_clicked(".")
            return True

        if key == QtCore.Qt.Key.Key_Backspace:
            self.operation_clicked("backspace")
            return True

        if key == QtCore.Qt.Key.Key_Escape:
            self.operation_clicked("CE")
            return True

        return super().eventFilter(obj, event)

    # Show or hide the keypad.
    def showButtons(self, checked):
        self.buttonGridWidget.setVisible(checked)
        self.adjustSize()

    # Handle changes to the first input.
    def input1Changed(self, text):
        if self.converting:
            return

        self.currentInput = self.inputbox1
        self.convert(self.inputbox1, self.inputbox2)

    # Handle changes to the second input.
    def input2Changed(self, text):
        if self.converting:
            return

        self.currentInput = self.inputbox2
        self.convert(self.inputbox2, self.inputbox1)

    # Convert when the first unit changes.
    def unit1Changed(self):
        if self.converting:
            return

        if self.currentInput == self.inputbox2:
            self.convert(self.inputbox2, self.inputbox1)
        else:
            self.convert(self.inputbox1, self.inputbox2)

        self.updateUnitLabel()

    # Convert when the second unit changes.
    def unit2Changed(self):
        if self.converting:
            return

        if self.currentInput == self.inputbox2:
            self.convert(self.inputbox2, self.inputbox1)
        else:
            self.convert(self.inputbox1, self.inputbox2)

        self.updateUnitLabel()

    # Convert one input into the other.
    def convert(self, source, target):
        if self.converting:
            return

        self.converting = True

        try:
            text = source.text().strip()

            if not text:
                target.clear()
                return

            try:
                value = float(text)
            except ValueError:
                target.clear()
                return

            if source == self.inputbox1:
                fromUnit = self.PintUnit(self.combo1.currentText())
                toUnit = self.PintUnit(self.combo2.currentText())
            else:
                fromUnit = self.PintUnit(self.combo2.currentText())
                toUnit = self.PintUnit(self.combo1.currentText())

            result = (value * fromUnit).to(toUnit)
            target.setText(self.format_number(result.magnitude))

        finally:
            self.converting = False

    # Swap the units and their values.
    def swapUnits(self):
        self.converting = True

        try:
            unit1 = self.combo1.currentText()
            unit2 = self.combo2.currentText()

            value1 = self.inputbox1.text()
            value2 = self.inputbox2.text()

            self.combo1.setCurrentText(unit2)
            self.combo2.setCurrentText(unit1)

            self.inputbox1.setText(value2)
            self.inputbox2.setText(value1)

        finally:
            self.converting = False

        # Recalculate using the input that was being edited.
        if self.currentInput == self.inputbox2:
            self.inputbox2.setFocus()
            self.convert(self.inputbox2, self.inputbox1)
        else:
            self.inputbox1.setFocus()
            self.convert(self.inputbox1, self.inputbox2)

        self.updateUnitLabel()

    # Format converted numbers without unnecessary zeros.
    def format_number(self, value):
        if value != 0 and (abs(value) >= 1e12 or abs(value) < 1e-9):
            return f"{value:.10g}"

        text = f"{value:.10f}".rstrip("0").rstrip(".")

        return "0" if text == "-0" else text

    # Handle keypad number input.
    def number_clicked(self, value):
        lineEdit = self.currentInput or self.inputbox1
        self.currentInput = lineEdit

        current = lineEdit.text()

        if value == ".":
            if "." in current:
                return

            if not current:
                lineEdit.setText("0.")
                return

        if current == "0" and value != ".":
            lineEdit.setText(value)
        else:
            lineEdit.insert(value)

    # Handle keypad operations.
    def operation_clicked(self, value):
        lineEdit = self.currentInput or self.inputbox1
        self.currentInput = lineEdit

        if value == "CE":
            lineEdit.setText("0")
            return

        if value == "backspace":
            if lineEdit.text() in ("", "0"):
                lineEdit.setText("0")
                return

            lineEdit.backspace()

            if not lineEdit.text():
                lineEdit.setText("0")

    # Update the unit comparison label.
    def updateUnitLabel(self):
        try:
            fromUnit = self.PintUnit(self.combo1.currentText())
            toUnit = self.PintUnit(self.combo2.currentText())

            result = (1 * fromUnit).to(toUnit)
            converted = self.format_number(result.magnitude)

            unit1 = self.unitDisplayName(self.combo1.currentText())
            unit2 = self.unitDisplayName(self.combo2.currentText())

            #self.inputbox1.s(unit1)

            self.unitLbl.setText(
                f"1 {unit1} = {converted} {unit2}"
            )

        except Exception:
            self.unitLbl.clear()
