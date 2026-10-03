from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
from pint import UnitRegistry

Time_measurements = [
    "Nanosecond",
    "Microsecond",
    "Millisecond",
    "Second",
    "Minute",
    "Hour",
    "Day",
    "Week",
    "Month",
    "Year",
    "Decade",
    "Century",
]


u = UnitRegistry()

u.define("fixed_month = 30 * day")
u.define("fixed_year = 365 * day")
u.define("fixed_decade = 10 * fixed_year")
u.define("fixed_century = 100 * fixed_year")


class TimeConversion(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.converting = False
        self.currentInput = None

        inputFont = QtGui.QFont("Arial", 18)
        comboFont = QtGui.QFont("Arial", 13)

        mainLayout = QtWidgets.QVBoxLayout(self)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(6)

        topRow = QtWidgets.QHBoxLayout()

        topRow.addStretch()
        mainLayout.addLayout(topRow)

        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d*\.?\d*"), self)

        self.inputbox1 = QtWidgets.QLineEdit("1")
        self.inputbox1.setFixedHeight(55)
        self.inputbox1.setFont(inputFont)
        self.inputbox1.setValidator(validator)
        self.inputbox1.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.inputbox1.textEdited.connect(self.input1Changed)
        self.inputbox1.installEventFilter(self)

        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFont(comboFont)
        self.combo1.setMinimumHeight(40)
        self.combo1.addItems(Time_measurements)
        self.combo1.currentTextChanged.connect(self.unit1Changed)

        self.swapButton = QtWidgets.QPushButton()
        self.swapButton.setFixedSize(35, 35)
        self.swapButton.setIcon(qta.icon("fa5s.exchange-alt"))
        self.swapButton.setIconSize(QtCore.QSize(15, 15))
        self.swapButton.setToolTip("Swap units (Ctrl+U)")
        self.swapButton.clicked.connect(self.swapUnits)

        swapShortcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        swapShortcut.activated.connect(self.swapUnits)

        self.inputbox2 = QtWidgets.QLineEdit("0")
        self.inputbox2.setFixedHeight(55)
        self.inputbox2.setFont(inputFont)
        self.inputbox2.setValidator(validator)
        self.inputbox2.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        self.inputbox2.textEdited.connect(self.input2Changed)
        self.inputbox2.installEventFilter(self)

        self.combo2 = QtWidgets.QComboBox()
        self.combo2.setFont(comboFont)
        self.combo2.setMinimumHeight(40)
        self.combo2.addItems(Time_measurements)
        self.combo2.currentTextChanged.connect(self.unit2Changed)

        self.unitLbl = QtWidgets.QLabel()
        self.unitLbl.setFont(QtGui.QFont("Arial", 12))
        self.unitLbl.setStyleSheet("color: gray;")
        self.unitLbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

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

        self.currentInput = self.inputbox1

        self.updateUnitLabel()
        self.convert(self.inputbox1, self.inputbox2)

    def PintUnit(self, unit_name):
        units = {
            "Nanosecond": u.nanosecond,
            "Microsecond": u.microsecond,
            "Millisecond": u.millisecond,
            "Second": u.second,
            "Minute": u.minute,
            "Hour": u.hour,
            "Day": u.day,
            "Week": u.week,
            "Month": u.fixed_month,
            "Year": u.fixed_year,
            "Decade": u.fixed_decade,
            "Century": u.fixed_century,
        }

        return units[unit_name]

    def unitDisplayName(self, unit_name):
        names = {
            "Nanosecond": "nanoseconds",
            "Microsecond": "microseconds",
            "Millisecond": "milliseconds",
            "Second": "seconds",
            "Minute": "minutes",
            "Hour": "hours",
            "Day": "days",
            "Week": "weeks",
            "Month": "months",
            "Year": "years",
            "Decade": "decades",
            "Century": "centuries",
        }

        return names[unit_name]

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Type.FocusIn:
            if obj in (self.inputbox1, self.inputbox2):
                self.currentInput = obj

        if event.type() != QtCore.QEvent.Type.KeyPress:
            return super().eventFilter(obj, event)

        if not isinstance(obj, QtWidgets.QLineEdit):
            return super().eventFilter(obj, event)

        modifiers = event.modifiers()

        if modifiers & (QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.AltModifier):
            return super().eventFilter(obj, event)

        self.currentInput = obj

        key = event.key()
        text = event.text()

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

    def input1Changed(self, text):
        if self.converting:
            return

        self.currentInput = self.inputbox1
        self.convert(self.inputbox1, self.inputbox2)

    def input2Changed(self, text):
        if self.converting:
            return

        self.currentInput = self.inputbox2
        self.convert(self.inputbox2, self.inputbox1)

    def unit1Changed(self):
        if self.converting:
            return

        self.updateUnitLabel()
        self.convertFromCurrentInput()

    def unit2Changed(self):
        if self.converting:
            return

        self.updateUnitLabel()
        self.convertFromCurrentInput()

    def convertFromCurrentInput(self):
        if self.currentInput == self.inputbox2:
            self.convert(self.inputbox2, self.inputbox1)
        else:
            self.convert(self.inputbox1, self.inputbox2)

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

            if source is self.inputbox1:
                fromUnit = self.PintUnit(self.combo1.currentText())
                toUnit = self.PintUnit(self.combo2.currentText())
            else:
                fromUnit = self.PintUnit(self.combo2.currentText())
                toUnit = self.PintUnit(self.combo1.currentText())

            result = (value * fromUnit).to(toUnit)
            target.setText(self.format_number(result.magnitude))

        except Exception:
            target.clear()

        finally:
            self.converting = False

    def swapUnits(self):
        unit1 = self.combo1.currentText()
        unit2 = self.combo2.currentText()

        value1 = self.inputbox1.text()
        value2 = self.inputbox2.text()

        previousInput = self.currentInput

        self.converting = True

        try:
            self.combo1.setCurrentText(unit2)
            self.combo2.setCurrentText(unit1)

            self.inputbox1.setText(value2)
            self.inputbox2.setText(value1)

        finally:
            self.converting = False

        if previousInput is self.inputbox2:
            self.currentInput = self.inputbox2
            self.inputbox2.setFocus()
        else:
            self.currentInput = self.inputbox1
            self.inputbox1.setFocus()

        self.convertFromCurrentInput()
        self.updateUnitLabel()

    def format_number(self, value):
        if value == 0:
            return "0"

        if abs(value) >= 1e12 or abs(value) < 1e-9:
            return f"{value:.10g}"

        text = f"{value:.10f}".rstrip("0").rstrip(".")

        if text in ("-0", ""):
            return "0"

        return text

    def number_clicked(self, value):
        lineEdit = self.currentInput or self.inputbox1
        self.currentInput = lineEdit

        current = lineEdit.text()

        if value == ".":
            if "." in current:
                return

            if not current:
                lineEdit.setText("0.")
                lineEdit.setFocus()
                return

        if current == "0" and value != ".":
            lineEdit.setText(value)
        else:
            lineEdit.insert(value)

        lineEdit.setFocus()

    def operation_clicked(self, value):
        lineEdit = self.currentInput or self.inputbox1
        self.currentInput = lineEdit

        if value == "CE":
            lineEdit.setText("0")
            lineEdit.setFocus()
            return

        if value == "backspace":
            text = lineEdit.text()

            if not text or text == "0":
                lineEdit.setText("0")
                return

            lineEdit.backspace()

            if not lineEdit.text():
                lineEdit.setText("0")

            lineEdit.setFocus()

    def updateUnitLabel(self):
        try:
            fromUnit = self.PintUnit(self.combo1.currentText())
            toUnit = self.PintUnit(self.combo2.currentText())

            result = (1 * fromUnit).to(toUnit)
            converted = self.format_number(result.magnitude)

            unit1 = self.unitDisplayName(self.combo1.currentText())
            unit2 = self.unitDisplayName(self.combo2.currentText())

            self.unitLbl.setText(f"1 {unit1} = {converted} {unit2}")
        except Exception:
            self.unitLbl.clear()