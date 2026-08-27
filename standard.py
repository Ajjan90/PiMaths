from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLabel
import qtawesome as qta

#The calculators and its other menus
class StandardCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Calculator state
        self.Num1 = None
        self.Operator = None
        self.Num2 = None
        self.waiting_for_num2 = False

        layout = QtWidgets.QVBoxLayout(self)
        TopRow = QtWidgets.QHBoxLayout()
        MainRow = QtWidgets.QVBoxLayout()

        self.Lbl = QtWidgets.QLabel("Standard")
        fontType = QtGui.QFont("Arial", 14)
        fontType.setBold(True)
        self.Lbl.setFont(fontType)

        self.HisBtn = QtWidgets.QPushButton()
        self.HisBtn.setIcon(qta.icon("fa5s.history"))
        self.HisBtn.setIconSize(QtCore.QSize(15, 15))
        self.HisBtn.setToolTip("History")
        self.HisBtn.setFixedSize(40, 40)

        self.CalTxt = QtWidgets.QLineEdit("0")
        self.CalTxt.setFixedHeight(55)
        self.CalTxt.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        TxtFont = QtGui.QFont("Arial", 25)
        self.CalTxt.setFont(TxtFont)
        validator = QtGui.QDoubleValidator(0, 999999, 10)
        self.CalTxt.setValidator(validator)

        self.calTrackerLbl = QtWidgets.QLabel("0+0")
        smallLbl = QtGui.QFont("Arial", 10)
        self.calTrackerLbl.setStyleSheet("color: gray;")
        self.calTrackerLbl.setFont(smallLbl)
        self.calTrackerLbl.setVisible(False)

        ButtonGrid = QtWidgets.QGridLayout()
        BtnFont = QtGui.QFont("Arial", 15)

        buttons = [
            ["%", "CE", "C", "backspace"],
            ["1/x", "x²", "√x", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],]

        for row, button_row in enumerate(buttons):
            for col, text in enumerate(button_row):

                button = QtWidgets.QPushButton()
                button.setFont(BtnFont)
                button.setFixedHeight(50)

                if text == "backspace":
                    button.setIcon(qta.icon("fa5s.backspace"))
                    button.setIconSize(QtCore.QSize(18, 18))

                    button.clicked.connect(lambda _, v=text: self.operation_clicked(v))
                else:
                    button.setText(text)

                    # Style equals button
                    if text == "=":
                        button.setStyleSheet(""" QPushButton {
                                background-color: #FF0033;
                                color: white;}

                            QPushButton:hover {
                                background-color: #CC0029;}

                            QPushButton:pressed {
                                background-color: #99001F; } """)

                    # Number buttons
                    if text.isdigit() or text == ".":
                        button.clicked.connect(lambda _, v=text: self.number_clicked(v))
                    # Operation buttons
                    else:
                        button.clicked.connect(lambda _, v=text: self.operation_clicked(v))

                ButtonGrid.addWidget(button, row, col)

        layout.addLayout(TopRow)
        layout.addLayout(MainRow)

        TopRow.addWidget(self.Lbl)
        TopRow.addWidget(self.HisBtn)

        MainRow.addWidget(self.CalTxt)
        MainRow.addWidget(self.calTrackerLbl, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.setAlignment(MainRow, QtCore.Qt.AlignmentFlag.AlignTop)
        layout.addLayout(ButtonGrid)

    # Number buttons
    def number_clicked(self, number):
        current = self.CalTxt.text()

        if self.waiting_for_num2:
            self.CalTxt.setText(number)
            self.waiting_for_num2 = False
            return

        if number == "." and "." in current:
            return

        if current == "0" and number != ".":
            self.CalTxt.setText(number)
        else:
            self.CalTxt.setText(current + number)

    # Operations
    def operation_clicked(self, operation):
        current_text = self.CalTxt.text()

        # Clear
        if operation == "C":
            self.Num1 = None
            self.Num2 = None
            self.Operator = None

            self.CalTxt.setText("0")
            self.calTrackerLbl.setText("")
            self.calTrackerLbl.setVisible(False)
            self.waiting_for_num2 = False
            return

        # Clear Entry
        if operation == "CE":
            self.CalTxt.setText("0")
            self.waiting_for_num2 = False
            return

        # Backspace
        if operation == "backspace":
            current = self.CalTxt.text()

            # If we're displaying an error, just reset it
            if current == "Error":
                self.CalTxt.setText("0")
                return

            if len(current) > 1:
                self.CalTxt.setText(current[:-1])
            else:
                self.CalTxt.setText("0")

            return

        # Make sure we have a valid number
        try:
            current_number = float(current_text)
        except ValueError:
            self.CalTxt.setText("Error")
            return

        # Positive / Negative
        if operation == "±":

            if current_number != 0:
                current_number *= -1

            self.CalTxt.setText(self.format_number(current_number))
            return

        # Percentage
        if operation == "%":
            result = current_number / 100
            self.CalTxt.setText(self.format_number(result))

            return

        # 1/x
        if operation == "1/x":
            if current_number == 0:
                self.CalTxt.setText("Error")
                return

            result = 1 / current_number
            self.calTrackerLbl.setText(f"1/({current_number})")
            self.calTrackerLbl.setVisible(True)
            self.CalTxt.setText(self.format_number(result))
            return

        # x²
        if operation == "x²":
            result = current_number ** 2        
            self.calTrackerLbl.setText(f"sqr({current_number})")
            self.calTrackerLbl.setVisible(True)
            self.CalTxt.setText(self.format_number(result))
            return

        # √x
        if operation == "√x":
            if current_number < 0:
                self.CalTxt.setText("Error")
                return

            result = current_number ** 0.5
            self.calTrackerLbl.setText(f"√({current_number})")
            self.calTrackerLbl.setVisible(True)
            self.CalTxt.setText(self.format_number(result))
            return

        # Equals
        if operation == "=":
            if self.Num1 is None or self.Operator is None:
                return

            self.Num2 = current_number
            result = self.calculate(self.Num1,self.Operator,self.Num2)

            if result is None:
                self.CalTxt.setText("Error")
                return

            self.calTrackerLbl.setText(f"{self.format_number(self.Num1)} " f"{self.Operator} " f"{self.format_number(self.Num2)}")
            self.CalTxt.setText(self.format_number(result))

            self.Num1 = result
            self.Num2 = None
            self.Operator = None
            self.waiting_for_num2 = True
            return

        # Arithmetic operators
        if operation in ["+", "−", "×", "÷"]:
            # If there is already an operation,
            # calculate it first.
            if self.Num1 is not None and self.Operator is not None:
                self.Num2 = current_number

                result = self.calculate(self.Num1, self.Operator, self.Num2)

                if result is None:
                    self.CalTxt.setText("Error")
                    return

                self.Num1 = result
                self.CalTxt.setText(self.format_number(result))
            else:
                self.Num1 = current_number

            self.Operator = operation
            self.waiting_for_num2 = True

            self.calTrackerLbl.setText(f"{self.format_number(self.Num1)} {operation}")
            self.calTrackerLbl.setVisible(True)

    # Perform calculation
    def calculate(self, num1, operator, num2):
        if operator == "+":
            return num1 + num2
        elif operator == "−":
            return num1 - num2
        elif operator == "×":
            return num1 * num2
        elif operator == "÷":
            if num2 == 0:
                return None

            return num1 / num2

        return None

    # Format numbers nicely
    def format_number(self, number):

        if number == int(number):
            return str(int(number))

        return str(number)