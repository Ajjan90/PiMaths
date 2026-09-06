from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
import pint

area_measurements = ["Millimeters", "Centimeters", "Meters", "Kilometers", "Inches","Feet", "Acre", "Hectare"]

class AreaCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        MainLayout = QtWidgets.QVBoxLayout(self)
        TopRow = QtWidgets.QHBoxLayout()

        # Fonts
        spinboxFont = QtGui.QFont("Arial", 20)
        comboFont = QtGui.QFont("Arial", 13)

        # Title
        self.Lbl = QtWidgets.QLabel("Area")
        font = QtGui.QFont("Arial", 14)
        font.setBold(True)
        self.Lbl.setFont(font)

        # Show buttons checkbox
        self.toggleBtn = QtWidgets.QCheckBox("Show buttons")
        self.toggleBtn.toggled.connect(self.showButtons)

        # Validator - numbers and one decimal point only
        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d*\.?\d*"))

        # First input
        self.inputbox1 = QtWidgets.QLineEdit()
        self.inputbox1.setFixedHeight(55)
        self.inputbox1.setFont(spinboxFont)
        self.inputbox1.setValidator(validator)
        self.inputbox1.setText("0")

        # First combo
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFont(comboFont)

        # Second input
        self.inputbox2 = QtWidgets.QLineEdit()
        self.inputbox2.setFixedHeight(55)
        self.inputbox2.setFont(spinboxFont)
        self.inputbox2.setValidator(validator)
        self.inputbox2.setText("0")

        # Second combo
        self.combo2 = QtWidgets.QComboBox()
        self.combo2.setFont(comboFont)

        for item in area_measurements:
            self.combo1.addItem(item)
            self.combo2.addItem(item)

        # Track which input is active
        self.currentInput = self.inputbox1
        self.inputbox1.focusInEvent = self.create_focus_event(self.inputbox1)
        self.inputbox2.focusInEvent = self.create_focus_event(self.inputbox2)

        # Button grid
        self.buttonGridWidget = QtWidgets.QWidget()
        self.buttonGrid = QtWidgets.QGridLayout(self.buttonGridWidget)

        buttonFont = QtGui.QFont("Arial", 15)

        buttons = [
            ["CE", "backspace"],
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            ["0", ".", "="]
        ]

        for row, buttonRow in enumerate(buttons):
            for col, text in enumerate(buttonRow):
                button = QtWidgets.QPushButton()
                button.setFont(buttonFont)
                button.setFixedHeight(50)

                if text == "backspace":
                    button.setIcon(qta.icon("fa5s.backspace"))
                    button.setIconSize(QtCore.QSize(18, 18))
                    button.clicked.connect(lambda _, v=text: self.operation_clicked(v))
                else:
                    button.setText(text)
                    if text == "=":
                        button.setStyleSheet("""
                            QPushButton {
                                background-color: #FF0033;
                                color: white;
                            }

                            QPushButton:hover {
                                background-color: #CC0029;
                            }

                            QPushButton:pressed {
                                background-color: #99001F;
                            }
                        """)

                    if text.isdigit() or text == ".":
                        button.clicked.connect(lambda _, v=text: self.number_clicked(v))
                    else:
                        button.clicked.connect(lambda _, v=text: self.operation_clicked(v))

                self.buttonGrid.addWidget(button, row, col)
        self.buttonGridWidget.setVisible(False)

        # Layout
        TopRow.addWidget(self.Lbl)
        TopRow.addStretch()
        TopRow.addWidget(self.toggleBtn)

        MainLayout.addLayout(TopRow)
        MainLayout.addWidget(self.inputbox1)
        MainLayout.addWidget(self.combo1)
        MainLayout.addSpacing(30)
        MainLayout.addWidget(self.inputbox2)
        MainLayout.addWidget(self.combo2)
        MainLayout.addWidget(self.buttonGridWidget)

    def create_focus_event(self, line_edit):
        original_focus_event = line_edit.focusInEvent

        def focus_event(event):
            self.currentInput = line_edit
            original_focus_event(event)
        return focus_event

    def showButtons(self, checked):
        self.buttonGridWidget.setVisible(checked)
        self.adjustSize()

    def number_clicked(self, value):
        line_edit = self.currentInput

        if line_edit is None:
            return

        current = line_edit.text()

        # Don't allow more than one decimal point
        if value == ".":
            if "." in current:
                return

        # Replace initial 0
        if current == "0" and value != ".":
            line_edit.setText(value)
        else:
            line_edit.insert(value)

    def operation_clicked(self, value):
        line_edit = self.currentInput

        if line_edit is None:
            return

        if value == "backspace":
            line_edit.backspace()
        elif value == "CE":
            line_edit.clear()
            line_edit.setText("0")
        elif value == "=":
            print("Equals pressed")