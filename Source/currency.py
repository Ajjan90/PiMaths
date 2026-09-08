from PySide6 import QtGui, QtWidgets, QtCore
import qtawesome as qta
import requests

url = "https://restcountries.com/v3.1/all?fields=name,currencies"
response = requests.get(url)
countries = response.json()

class CurrencyCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.converting = False
        self.currentInput = None # Track which input is being edited

        self.setMinimumWidth(380)

        MainLayout = QtWidgets.QVBoxLayout(self)
        MainLayout.setContentsMargins(10, 10, 10, 10)

        TopRow = QtWidgets.QHBoxLayout()

        # Fonts
        inputFont = QtGui.QFont("Arial", 18)
        comboFont = QtGui.QFont("Arial", 13)
        buttonFont = QtGui.QFont("Arial", 15)

        # Title
        self.Lbl = QtWidgets.QLabel("Currency")        
        titleFont = QtGui.QFont("Arial", 14)
        titleFont.setBold(True)
        self.Lbl.setFont(titleFont)

        self.toggleBtn = QtWidgets.QCheckBox("Show buttons")
        self.toggleBtn.setToolTip("Show buttons (Ctrl+I)")
        self.toggleBtn.toggled.connect(self.showButtons)
        # Create a keyborad shortcut for this action
        self.toggleShrtcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+I"), self)
        self.toggleShrtcut.activated.connect(self.toggleBtn.toggle)

        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d*\.?\d*"))

        # First input
        self.inputbox1 = QtWidgets.QLineEdit()
        self.inputbox1.setFixedHeight(55)
        self.inputbox1.setFont(inputFont)
        self.inputbox1.setValidator(validator)
        self.inputbox1.setText("1")

        # First combo
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFont(comboFont)
        self.combo1.setMinimumHeight(40)

        #Swap button
        self.swapButton = QtWidgets.QPushButton()
        self.swapButton.setFixedSize(35, 35)
        self.swapButton.setIcon(qta.icon("fa5s.exchange-alt"))
        self.swapButton.setIconSize(QtCore.QSize(15, 15))
        self.swapButton.setToolTip("Swap units (Ctrl+U)")
        self.swapButton.clicked.connect(self.swapUnits)
        #Implement the keyborad shortcut for the swapButton
        self.swapShtcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        self.swapShtcut.activated.connect(self.swapUnits)

        # Second input
        self.inputbox2 = QtWidgets.QLineEdit()
        self.inputbox2.setFixedHeight(55)
        self.inputbox2.setFont(inputFont)
        self.inputbox2.setValidator(validator)
        self.inputbox2.setText("0")

        # Second combo
        self.combo2 = QtWidgets.QComboBox()
        self.combo2.setFont(comboFont)
        self.combo2.setMinimumHeight(40)

        # Label to display what 1 unit is to the other unit
        self.unitLbl = QtWidgets.QLabel()
        self.unitLbl.setFont(QtGui.QFont("Arial", 12))

        # Add units
        #for item in area_measurements:
        #    self.combo1.addItem(item)
        #    self.combo2.addItem(item)

        # Default units
        #self.combo1.setCurrentText("Square Meters")
        #self.combo2.setCurrentText("Square Feet")

        # Connect conversion signals
        #self.inputbox1.textChanged.connect(self.input1Changed)
        #self.inputbox2.textChanged.connect(self.input2Changed)
        #self.combo1.currentTextChanged.connect(self.unit1Changed)
        #self.combo2.currentTextChanged.connect(self.unit2Changed)

        # Update the 1-unit comparison label
        #self.combo1.currentTextChanged.connect(self.updateUnitLabel)
        #self.combo2.currentTextChanged.connect(self.updateUnitLabel)

        # Button grid
        self.buttonGridWidget = QtWidgets.QWidget()
        self.buttonGrid = QtWidgets.QGridLayout(self.buttonGridWidget)
        self.buttonGrid.setContentsMargins(0, 10, 0, 0)
        self.buttonGrid.setSpacing(5)

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

                # Backspace
                if text == "backspace":
                    button.setIcon(qta.icon("fa5s.backspace"))
                    button.setIconSize(QtCore.QSize(18, 18))
                    button.clicked.connect(lambda _, v=text:self.operation_clicked(v))
                else:
                    button.setText(text)
                    if text.isdigit() or text == ".":
                        button.clicked.connect(lambda _, v=text:self.number_clicked(v))
                    else:
                        button.clicked.connect(lambda _, v=text:self.operation_clicked(v))
                self.buttonGrid.addWidget(button,row,col)

        # Hide keypad initially
        self.buttonGridWidget.setVisible(False)

        # Layout
        TopRow.addWidget(self.Lbl)
        TopRow.addStretch()
        TopRow.addWidget(self.toggleBtn)

        MainLayout.addLayout(TopRow)

        # First conversion
        MainLayout.addWidget(self.inputbox1)
        MainLayout.addWidget(self.combo1)

        SwapLayout = QtWidgets.QHBoxLayout()

        SwapLayout.addStretch()
        SwapLayout.addWidget(self.swapButton)
        SwapLayout.addStretch()

        MainLayout.addLayout(SwapLayout)
        MainLayout.addWidget(self.inputbox2)
        MainLayout.addWidget(self.combo2)
        MainLayout.addWidget(self.unitLbl)
        MainLayout.addWidget(self.buttonGridWidget)

    # Focus tracking
    def FocusEvent(self, line_edit):
        original_focus_event = line_edit.focusInEvent

        def focus_event(event):
            self.currentInput = line_edit
            original_focus_event(event)
        return focus_event

    # Show the buttongrid
    def showButtons(self, checked):
        self.buttonGridWidget.setVisible(checked)
        self.adjustSize()
    
    # Swap units
    def swapUnits(self):
        # Prevent combo box signals from converting
        self.converting = True

        try:
            # Save current units
            unit1 = self.combo1.currentText()
            unit2 = self.combo2.currentText()

            # Save current values
            value1 = self.inputbox1.text()
            value2 = self.inputbox2.text()

            # Swap units
            index1 = self.combo1.findText(unit2)
            index2 = self.combo2.findText(unit1)

            if index1 >= 0:
                self.combo1.setCurrentIndex(index1)

            if index2 >= 0:
                self.combo2.setCurrentIndex(index2)

            # Swap values
            self.inputbox1.setText(value2)
            self.inputbox2.setText(value1)
        finally:
            self.converting = False

        # Keep the field that was being edited active
        if self.currentInput == self.inputbox1:
            self.inputbox1.setFocus()
            self.convertFirst()
        else:
            self.inputbox2.setFocus()
            self.convertSecond()

    # Number formatting
    def format_number(self, value):
        # Scientific notation for very large/small numbers
        if value != 0 and (abs(value) >= 1e12 or abs(value) < 1e-9):
            return f"{value:.10g}"

        # Normal number
        text = (f"{value:.10f}".rstrip("0").rstrip("."))

        if text == "-0":
            text = "0"
        return text

    # Number keypad
    def number_clicked(self, value):
        line_edit = self.currentInput

        if line_edit is None:
            line_edit = self.inputbox1
            self.currentInput = line_edit

        current = line_edit.text()

        # Decimal point
        if value == ".":
            if "." in current:
                return

            if current == "":
                line_edit.setText("0.")
                return

        # Replace initial zero
        if current == "0" and value != ".":
            line_edit.setText(value)
        else:
            line_edit.insert(value)

    # Calculator operations
    def operation_clicked(self, value):
        line_edit = self.currentInput

        if line_edit is None:
            line_edit = self.inputbox1
            self.currentInput = line_edit

        # Backspace
        if value == "backspace":
            current = line_edit.text()
            if len(current) <= 1:
                line_edit.setText("0")
            else:
                line_edit.backspace()

                if line_edit.text() == "":
                    line_edit.setText("0")
        # Clear entry
        elif value == "CE":
            line_edit.setText("0")

    #Update the unitLbl when the user changes unit measurements
    def updateUnitLabel(self):
        try:
            from_unit = self.PintUnit(self.combo1.currentText())
            to_unit = self.PintUnit(self.combo2.currentText())

            result = (1 * from_unit).to(to_unit)

            converted = self.format_number(result.magnitude)

            self.unitLbl.setText(
                f"1 {self.unitDisplayName(self.combo1.currentText())} = "f"{converted} {self.unitDisplayName(self.combo2.currentText())}"
            )
        except Exception:
            self.unitLbl.setText("")