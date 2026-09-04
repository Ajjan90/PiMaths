from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLineEdit
import qtawesome as qta
import ast
import math
import operator
import re

from Window.helpWin import HelpWindow

class PaperCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QtWidgets.QVBoxLayout(self)
        topRow = QtWidgets.QHBoxLayout()

        titleFont = QtGui.QFont("Arial", 14)
        titleFont.setBold(True)

        inputFont = QtGui.QFont("Arial", 15)

        outputFont = QtGui.QFont("Arial", 15)
        outputFont.setBold(True)

        # Title
        self.Lbl = QtWidgets.QLabel("Paper Mode")
        self.Lbl.setFont(titleFont)

        # More options button
        self.moreBtn = QtWidgets.QPushButton()
        self.moreBtn.setIcon(qta.icon("ri.more-2-fill"))
        self.moreBtn.setIconSize(QtCore.QSize(20, 20))
        self.moreBtn.setToolTip("More options")
        self.moreBtn.setFixedSize(40, 40)

        # Create dropdown menu
        self.moreMenu = QtWidgets.QMenu(self.moreBtn)

        # Clear paper action
        moreClr = QtGui.QAction("Clear paper", self.moreMenu)
        moreClr.setShortcut("Ctrl+Space")
        moreClr.triggered.connect(self.clearListbox)

        # Copy all action
        moreCopy = QtGui.QAction("Copy all", self.moreMenu)
        moreCopy.setShortcut("Ctrl+Shift+C")
        moreCopy.triggered.connect(self.copyAllClip)

        # Add actions to menu
        self.moreMenu.addAction(moreClr)
        self.moreMenu.addAction(moreCopy)

        # Attach menu to button
        self.moreBtn.setMenu(self.moreMenu)

        # Help Button
        self.helpBtn = QtWidgets.QPushButton()
        self.helpBtn.setIcon(qta.icon("mdi6.help"))
        self.helpBtn.setIconSize(QtCore.QSize(20, 20))
        self.helpBtn.setToolTip("Help")
        self.helpBtn.setFixedSize(40, 40)
        self.helpBtn.clicked.connect( self.showHelpWindow)

        # Listbox
        self.listOutput = QtWidgets.QListWidget()
        self.listOutput.setSpacing(3)

        # Input area
        inputLayout = QtWidgets.QHBoxLayout()
        self.inputBox = QLineEdit()
        self.inputBox.setFont(inputFont)
        self.inputBox.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)
        self.inputBox.setPlaceholderText("Enter calculation...")
        self.inputBox.returnPressed.connect(self.calculate)

        # Enter button
        enterBtn = QtWidgets.QPushButton("=")
        enterBtn.setFixedSize(40, 35)
        enterBtn.setFont(outputFont)

        enterBtn.setStyleSheet("""
            QPushButton {
                background-color: #FF0033;
                color: white;
                border: none;
                border-radius: 4px;
            }

            QPushButton:hover {
                background-color: #CC0029;
            }

            QPushButton:pressed {
                background-color: #99001F;
            }
        """)

        enterBtn.clicked.connect(self.calculate)

        # Layout
        topRow.addWidget(self.Lbl)
        topRow.addStretch()
        topRow.addWidget(self.moreBtn)
        topRow.addWidget(self.helpBtn)

        inputLayout.addWidget(self.inputBox)
        inputLayout.addWidget(enterBtn)

        mainLayout.addLayout(topRow)
        mainLayout.addWidget(self.listOutput)
        mainLayout.addLayout(inputLayout)

    # Calculator
    def calculate(self):
        expression = self.inputBox.text().strip()

        if not expression:
            return

        try:
            result = SafeCalculator.calculate(expression)
            resultText = self.formatResult(result)

            # Input item
            inputItem = QtWidgets.QListWidgetItem(expression)

            inputItem.setFont(QtGui.QFont("Arial", 15))
            inputItem.setData(QtCore.Qt.ItemDataRole.UserRole,expression)

            # Result item
            outputItem = QtWidgets.QListWidgetItem(resultText)

            outputFont = QtGui.QFont("Arial", 15)
            outputFont.setBold(True)

            outputItem.setFont(outputFont)
            outputItem.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)

            # Add to paper
            self.listOutput.addItem(inputItem)
            self.listOutput.addItem(outputItem)

            self.listOutput.scrollToBottom()

            # Clear input
            self.inputBox.clear()
            self.inputBox.setFocus()
        except ValueError as error:
            self.showError(str(error))

    # Format result
    def formatResult(self, result):
        if isinstance(result, float):
            if result.is_integer():
                return str(int(result))

            return f"{result:.12g}"
        return str(result)

    # Show error
    def showError(self, message):
        errorItem = QtWidgets.QListWidgetItem(f"Error: {message}")

        errorFont = QtGui.QFont("Arial", 13)
        errorFont.setItalic(True)

        errorItem.setFont(errorFont)
        errorItem.setForeground(QtGui.QBrush(QtGui.QColor("#FF0033")))

        self.listOutput.addItem(errorItem)
        self.listOutput.scrollToBottom()

        self.inputBox.selectAll()
        self.inputBox.setFocus()

    # Focus input
    def focusInput(self):
        self.inputBox.setFocus()
        self.inputBox.setCursorPosition(len(self.inputBox.text()))

    # Clear paper
    def clearListbox(self):
        self.listOutput.clear()
        self.inputBox.setFocus()

    # Copy all the item form the Listbox
    def copyAllClip(self):
        if self.listOutput.count() == 0:
            return

        lines = []

        # Go through every item
        for i in range(self.listOutput.count()):
            item = self.listOutput.item(i)
            text = item.text().strip()

            if not text:
                continue

            if i % 2 == 0:
                # Expression
                lines.append(text)
            else:
                # Result
                lines.append(f"= {text}")

        clipboardText = "\n".join(lines)
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(clipboardText)

    def showHelpWindow(self):
        self.helpWindow = HelpWindow()
        self.helpWindow.show()

#A class that teaches the paper mode calculator what to do and how to calculate an expression, provide error handling messages and more.
class SafeCalculator:
    CONSTANTS = {
        "pi": math.pi, #3.14...
        "π": math.pi, #3.14...
        "e": math.e, #2.71...
        "tau": math.tau, #6.28...
    }

    FUNCTIONS = {
        "sqrt": math.sqrt, #x^2
        "sin": lambda x: math.sin(math.radians(x)), #sin
        "cos": lambda x: math.cos(math.radians(x)), #cos
        "tan": lambda x: math.tan(math.radians(x)), #tan
        "asin": lambda x: math.degrees(math.asin(x)), #asin
        "acos": lambda x: math.degrees(math.acos(x)), #acos
        "atan": lambda x: math.degrees(math.atan(x)), #atan
        "log": math.log10, #Log10
        "ln": math.log, #Log
    }

    OPERATORS = {
        ast.Add: operator.add, #+
        ast.Sub: operator.sub, #-
        ast.Mult: operator.mul, #*
        ast.Div: operator.truediv, #/
        ast.Pow: operator.pow, #power of
        ast.USub: operator.neg, #negative
        ast.UAdd: operator.pos, #positive
    }
    
    @classmethod
    def calculate(cls, expression):
        expression = expression.strip() #to break down the expression or the user input

        if not expression:
            raise ValueError("Enter a calculation")

        #Replace a symbol based on the following instructions 
        expression = expression.replace("×", "*")
        expression = expression.replace("÷", "/")
        expression = expression.replace("^", "**")
        expression = expression.replace("PI", "pi")
        expression = cls.convert_factorials(expression)
        expression = cls.add_implicit_multiplication(expression)

        try:
            tree = ast.parse(expression, mode="eval")
            result = cls._evaluate(tree.body)

            if isinstance(result, complex):
                raise ValueError("Complex numbers are not supported")

            if not math.isfinite(float(result)):
                raise ValueError("Result is too large")

            return result
        except ZeroDivisionError:
            raise ValueError("Cannot divide by zero")
        except ValueError as error:
            raise ValueError(str(error) or "Invalid expression")
        except (SyntaxError, TypeError, OverflowError):
            raise ValueError("Invalid expression")

    #Functions to convert the given expression to a factorials
    @classmethod
    def convert_factorials(cls, expression):
        expression = re.sub(r'(\d+(?:\.\d+)?)!',r'factorial(\1)',expression)
        pattern = re.compile(r'\(([^()]+)\)!')

        while pattern.search(expression):
            expression = pattern.sub(r'factorial(\1)',expression)
        return expression

    @classmethod
    def add_implicit_multiplication(cls, expression):
        expression = re.sub(r'(\d)(?=(pi|π|e|tau)\b)',r'\1*',expression)
        expression = re.sub(r'(pi|π|e|tau)(?=\d)',r'\1*',expression)
        expression = re.sub(r'(\d)\(',r'\1*(',expression)
        expression = re.sub(r'\)(?=\d)',r')*',expression)
        expression = re.sub(r'\)(?=(pi|π|e|tau)\b)',r')*',expression)
        expression = re.sub(r'(pi|π|e|tau)\(',r'\1*(',expression)
        return expression

    @classmethod
    def _evaluate(cls, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                return node.value
            raise ValueError("Invalid number")

        if isinstance(node, ast.Name):
            if node.id in cls.CONSTANTS:
                return cls.CONSTANTS[node.id]
            raise ValueError(f"Unknown value: {node.id}")

        if isinstance(node, ast.BinOp):
            operation = cls.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not supported")

            left = cls._evaluate(node.left)
            right = cls._evaluate(node.right)

            if isinstance(node.op, ast.Pow):
                if abs(right) > 1000:
                    raise ValueError("Power is too large")
                if abs(left) > 1_000_000 and abs(right) > 10:
                    raise ValueError("Power is too large")

            return operation(left, right)

        if isinstance(node, ast.UnaryOp):
            operation = cls.OPERATORS.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not supported")

            return operation(cls._evaluate(node.operand))

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function")

            function_name = node.func.id

            if function_name == "factorial":
                if len(node.args) != 1:
                    raise ValueError("factorial() requires one value")

                value = cls._evaluate(node.args[0])

                if not float(value).is_integer():
                    raise ValueError("Factorial requires a whole number")

                value = int(value)

                if value < 0:
                    raise ValueError("Factorial requires a positive number")

                if value > 1000:
                    raise ValueError("Factorial is too large")

                return math.factorial(value)

            function = cls.FUNCTIONS.get(function_name)

            if function is None:
                raise ValueError(f"Unknown function: {function_name}")

            if len(node.args) != 1:
                raise ValueError(f"{function_name}() requires one value")

            return function(cls._evaluate(node.args[0]))

        raise ValueError("Invalid expression")