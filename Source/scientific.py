#The scientific calculator's code uses the same code as the Standard calculator's code but with more features added

from PySide6 import QtWidgets, QtCore, QtGui
#from Main import MainWindow
import qtawesome as qta
import math

#to store the calculation into this List
CalHisList = []

class ScientificCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.Num1 = None
        self.Operator = None
        self.Num2 = None
        self.waiting_for_num2 = False
        # Bracket / expression variables
        self.expression = ""
        self.bracket_count = 0
        self.using_expression = False

        mainLayout = QtWidgets.QHBoxLayout(self) #This will hold the Main content layout and the History layout
        layout = QtWidgets.QVBoxLayout() #The layout for the Main Content
        topRow = QtWidgets.QHBoxLayout() #This is for the Top row like Label and Button
        mainRow = QtWidgets.QVBoxLayout() # For the textbox and the Button grid

        #The Title 
        self.Lbl = QtWidgets.QLabel("Scientific")
        font = QtGui.QFont("Arial", 14)
        font.setBold(True)
        self.Lbl.setFont(font)

        #Button to toggle the history sidepanel
        self.HisBtn = QtWidgets.QPushButton()
        self.HisBtn.setIcon(qta.icon("fa5s.history")) #set the icon as the history icon
        self.HisBtn.setIconSize(QtCore.QSize(15, 15))
        self.HisBtn.setToolTip("History")
        self.HisBtn.setFixedSize(40, 40)
        self.HisBtn.clicked.connect(self.toggle_history_panel)

        #The Textbox to run and display calculations
        self.CalTxt = QtWidgets.QLineEdit("0")
        self.CalTxt.setFixedHeight(55)
        self.CalTxt.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.CalTxt.setFont(QtGui.QFont("Arial", 25))
        self.CalTxt.setReadOnly(True) #This will prevent users from typing non-digit inputs

        #Small label underneath the textbox to display the calculations
        self.calTrackerLbl = QtWidgets.QLabel()
        self.calTrackerLbl.setFont(QtGui.QFont("Arial", 10))
        self.calTrackerLbl.setStyleSheet("color: gray;")
        self.calTrackerLbl.setVisible(False)

        #Trigonometry, Memory
        self.ComboRow = QtWidgets.QHBoxLayout() #To hold the comboboxes

        #Trigonometry Combobox with Sin,Cos,Tan and its other -1 components
        self.TriCombo = QtWidgets.QComboBox()
        self.TriCombo.setPlaceholderText("Trigonometry options")
        self.TriCombo.addItems(["sin", "cos", "tan", "sin-1", "cos-1", "tan-1"])
        self.TriCombo.insertSeparator(3)

        self.MemCombo = QtWidgets.QComboBox()
        self.MemCombo.setPlaceholderText("Memory options")
        self.MemCombo.addItems(["MC (Memory Clear)", "MR (Memory Reset)", "M+ (Memory Add)", "M- (Memory Subtract)", "MS (Memory Store)"])        

        #Add the Trigonometry and the Memory combobox into the row
        self.ComboRow.addWidget(self.TriCombo)
        self.ComboRow.addWidget(self.MemCombo)

        #The grid layout for the buttons
        buttonGrid = QtWidgets.QGridLayout()
        buttonFont = QtGui.QFont("Arial", 15)

        buttons = [
            ["x³", "π", "e", "(", ")"],
            ["³√x", "%", "CE", "C", "backspace"],
            ["n!", "1/x", "x²", "√x", "÷"],
            ["x^y", "7", "8", "9", "×"],
            ["ln", "4", "5", "6", "−"],
            ["log", "1", "2", "3", "+"],
            ["Rnd", "±", "0", ".", "="]
        ]

        #Display the buttons as listed on the buttons list
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

                    #If the button is a =, then set the backcolour to red
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

                buttonGrid.addWidget(button, row, col)

        #Add the Label and the Button to the TopRow
        topRow.addWidget(self.Lbl)
        topRow.addWidget(self.HisBtn)

        #Add the Textbox, Label and the buttongrid
        mainRow.addWidget(self.CalTxt)
        mainRow.addWidget(self.calTrackerLbl, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        mainRow.addLayout(self.ComboRow)
        mainRow.addLayout(buttonGrid)

        layout.addLayout(topRow)
        layout.addLayout(mainRow)

        # History panel
        self.historyPanel = QtWidgets.QFrame()

        self.historyPanel.setFrameShape(
            QtWidgets.QFrame.Shape.StyledPanel
        )

        self.historyPanel.setFrameShadow(
            QtWidgets.QFrame.Shadow.Raised
        )

        self.historyPanel.setMinimumWidth(300)


        # ==========================================================
        # Tab control
        # ==========================================================

        self.tabControl = QtWidgets.QTabWidget()

        # History tab
        self.HisTab = QtWidgets.QWidget()

        # Memory tab
        self.MemTab = QtWidgets.QWidget()

        # Add tabs
        self.tabControl.addTab(
            self.HisTab,
            "History"
        )

        self.tabControl.addTab(
            self.MemTab,
            "Memory"
        )


        # ==========================================================
        # History tab layout
        # ==========================================================

        historyLayout = QtWidgets.QVBoxLayout(
            self.HisTab
        )


        # ==========================================================
        # History top row
        # ==========================================================

        historyTopRow = QtWidgets.QHBoxLayout()


        # History title
        historyTitle = QtWidgets.QLabel(
            "History"
        )

        historyFont = QtGui.QFont(
            "Arial",
            14
        )

        historyFont.setBold(True)

        historyTitle.setFont(
            historyFont
        )


        # Clear history button
        self.DelBtn = QtWidgets.QPushButton()

        self.DelBtn.setIcon(
            qta.icon("fa5s.trash")
        )

        self.DelBtn.setIconSize(
            QtCore.QSize(15, 15)
        )

        self.DelBtn.setToolTip(
            "Clear All"
        )

        self.DelBtn.setFixedSize(
            40,
            40
        )

        self.DelBtn.clicked.connect(
            self.clear_history
        )


        # ==========================================================
        # History list
        # ==========================================================

        self.historyList = QtWidgets.QListWidget()

        self.historyList.setFont(
            QtGui.QFont(
                "Arial",
                11
            )
        )


        # Double-click history item
        self.historyList.itemDoubleClicked.connect(
            self.get_cal_item
        )


        # Context menu
        self.historyList.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.historyList.customContextMenuRequested.connect(
            self.show_history_context_menu
        )


        # ==========================================================
        # Copy action
        # ==========================================================

        self.copyAction = QtGui.QAction(
            "Copy",
            self
        )

        self.copyAction.setShortcut(
            QtGui.QKeySequence.Copy
        )

        self.copyAction.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut
        )

        self.copyAction.triggered.connect(
            self.copy_history_item
        )

        self.historyList.addAction(
            self.copyAction
        )


        # ==========================================================
        # Delete action
        # ==========================================================

        self.deleteAction = QtGui.QAction(
            "Delete",
            self
        )

        self.deleteAction.setShortcut(
            QtGui.QKeySequence.Delete
        )

        self.deleteAction.setShortcutContext(
            QtCore.Qt.ShortcutContext.WidgetShortcut
        )

        self.deleteAction.triggered.connect(
            self.delete_selected_history_item
        )

        self.historyList.addAction(
            self.deleteAction
        )


        # ==========================================================
        # Add widgets to History top row
        # ==========================================================

        historyTopRow.addWidget(
            historyTitle
        )

        historyTopRow.addStretch()

        historyTopRow.addWidget(
            self.DelBtn
        )


        # ==========================================================
        # Add History content to History tab
        # ==========================================================

        historyLayout.addLayout(
            historyTopRow
        )

        historyLayout.addWidget(
            self.historyList
        )


        # ==========================================================
        # Memory tab
        # ==========================================================
        #
        # Leave this empty for now.
        # You can add the Memory UI here later.
        #

        memoryLayout = QtWidgets.QVBoxLayout(
            self.MemTab
        )


        # ==========================================================
        # Put the TabWidget inside the History panel
        # ==========================================================

        historyPanelLayout = QtWidgets.QVBoxLayout(
            self.historyPanel
        )

        historyPanelLayout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        historyPanelLayout.addWidget(
            self.tabControl
        )


        # ==========================================================
        # Initially hide History panel
        # ==========================================================

        self.historyPanel.hide()


        # ==========================================================
        # Add calculator + history panel to main layout
        # ==========================================================

        mainLayout.addLayout(
            layout,
            3
        )

        mainLayout.addWidget(
            self.historyPanel,
            1
        )


        # ==========================================================
        # Event filter
        # ==========================================================

        QtWidgets.QApplication.instance().installEventFilter(
            self
        )


    #The function to run an keypress event
    #If the user uses the keyborad to input their calculations
    def eventFilter(self, obj, event):
        if event.type() != QtCore.QEvent.Type.KeyPress:
            return super().eventFilter(obj, event)

        key = event.key()
        text = event.text()
        focus = QtWidgets.QApplication.focusWidget()

        if focus == self.historyList:
            if key in (QtCore.Qt.Key.Key_Delete, QtCore.Qt.Key.Key_C) and event.modifiers() == QtCore.Qt.KeyboardModifier.NoModifier:
                return super().eventFilter(obj, event)
            if event.modifiers() & QtCore.Qt.KeyboardModifier.ControlModifier:
                return super().eventFilter(obj, event)

        if event.modifiers() & (QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.AltModifier):
            return super().eventFilter(obj, event)

        if text.isdigit():
            self.number_clicked(text)
            self.CalTxt.setFocus()
            return True

        if text == ".":
            self.number_clicked(".")
            self.CalTxt.setFocus()
            return True

        if text == "+":
            self.operation_clicked("+")
            self.CalTxt.setFocus()
            return True

        if text == "-":
            self.operation_clicked("−")
            self.CalTxt.setFocus()
            return True

        if text == "*":
            self.operation_clicked("×")
            self.CalTxt.setFocus()
            return True

        if text == "/":
            self.operation_clicked("÷")
            self.CalTxt.setFocus()
            return True

        if text == "%":
            self.operation_clicked("%")
            self.CalTxt.setFocus()
            return True

        if text == "=" or key in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
            self.operation_clicked("=")
            self.CalTxt.setFocus()
            return True

        if key == QtCore.Qt.Key.Key_Backspace:
            self.operation_clicked("backspace")
            self.CalTxt.setFocus()
            return True

        if key == QtCore.Qt.Key.Key_Escape:
            self.operation_clicked("C")
            self.CalTxt.setFocus()
            return True

        if key == QtCore.Qt.Key.Key_F9:
            self.operation_clicked("±")
            self.CalTxt.setFocus()
            return True

        return super().eventFilter(obj, event)

    #For the buttons, define what is being clicked as a number
    def number_clicked(self, number):

        current = self.CalTxt.text()

        # Expression mode
        if self.using_expression:
            if number == ".":
                current_number = ""
                for char in reversed(self.expression):
                    if char.isdigit() or char == ".":
                        current_number = (
                            char + current_number
                        )
                    else:
                        break
                if "." in current_number:
                    return

            if (
                self.expression
                and self.expression[-1] == ")"
            ):
                self.expression += "×"

            self.expression += number

            self.CalTxt.setText(
                self.expression
            )

            return

        # Normal calculator mode
        if self.waiting_for_num2:

            self.CalTxt.setText(
                number
            )

            self.waiting_for_num2 = False

            return

        # Prevent multiple decimal points
        if number == "." and "." in current:
            return

        # Replace initial zero
        if current == "0" and number != ".":
            self.CalTxt.setText(
                number
            )

        else:
            self.CalTxt.setText(
                current + number
            )

    #For the buttons, define what is being clicked as an operator like +-*/= C CE and others
    def operation_clicked(self, operation):
        current_text = self.CalTxt.text()

        # CLEAR
        if operation == "C":
            self.Num1 = None
            self.Num2 = None
            self.Operator = None

            self.expression = ""
            self.bracket_count = 0
            self.using_expression = False

            self.CalTxt.setText("0")

            self.calTrackerLbl.clear()
            self.calTrackerLbl.hide()

            self.waiting_for_num2 = False

            return

        # CLEAR ENTRY
        if operation == "CE":
            if self.using_expression:
                self.expression = ""
                self.bracket_count = 0
                self.using_expression = False

            self.CalTxt.setText("0")
            self.waiting_for_num2 = False

            return

        # BACKSPACE
        if operation == "backspace":
            if current_text == "Error":
                self.CalTxt.setText("0")

                self.expression = ""
                self.bracket_count = 0
                self.using_expression = False

                return

            # Expression mode
            if self.using_expression:
                if self.expression:
                    last_character = self.expression[-1]

                    if last_character == "(":
                        self.bracket_count -= 1

                    elif last_character == ")":
                        self.bracket_count += 1

                    self.expression = self.expression[:-1]

                if self.expression:
                    self.CalTxt.setText(self.expression)
                else:
                    self.CalTxt.setText("0")
                    self.using_expression = False
                return

            # Normal mode
            self.CalTxt.setText(
                current_text[:-1]
                if len(current_text) > 1
                else "0"
            )
            return

        # OPEN BRACKET
        if operation == "(":
            self.add_open_bracket()
            return

        # CLOSE BRACKET
        if operation == ")":
            self.add_close_bracket()
            return

        # EXPRESSION MODE
        if self.using_expression:
            # Equals
            if operation == "=":
                self.calculate_expression()
                return

            # Basic operators
            if operation in ("+", "−", "×", "÷"):
                # Don't allow an operator directly after
                # another operator or an opening bracket.
                if self.expression.endswith(("+", "−", "×", "÷", "(")):
                    return

                self.expression += operation
                self.CalTxt.setText(self.expression)
                return

            # π
            if operation == "π":
                # If expression ends with a number or ),
                # insert multiplication.
                if (self.expression and (self.expression[-1].isdigit()or self.expression[-1] == ")")):
                    self.expression += "×"

                self.expression += str(math.pi)
                self.CalTxt.setText(self.expression)

                return

            # e
            if operation == "e":
                if (self.expression and (self.expression[-1].isdigit()or self.expression[-1] == ")")):
                    self.expression += "×"

                self.expression += str(math.e)
                self.CalTxt.setText(self.expression)
                return

        # NORMAL CALCULATOR MODE
        try:
            current_number = float(current_text)
        except ValueError:
            self.CalTxt.setText("Error")
            return

        # PLUS / MINUS SIGN
        if operation == "±":
            current_number *= -1
            self.CalTxt.setText(self.format_number(current_number))
            return

        # PERCENT
        if operation == "%":
            result = current_number / 100
            self.CalTxt.setText(self.format_number(result))
            return

        # RECIPROCAL
        if operation == "1/x":
            if current_number == 0:
                self.CalTxt.setText("Error")
                return

            result = 1 / current_number

            number = self.format_number(current_number)
            resultText = self.format_number(result)
            self.calTrackerLbl.setText(f"1/({number})")
            self.calTrackerLbl.show()

            self.CalTxt.setText(resultText)
            CalHisList.insert(0, f"1/({number}) = {resultText}")
            self.UpdateHistoryList()
            return

        # SQUARE
        if operation == "x²":
            result = current_number ** 2
            number = self.format_number(current_number)
            resultText = self.format_number(result)
            self.calTrackerLbl.setText(f"sqr({number})")
            self.calTrackerLbl.show()
            self.CalTxt.setText(resultText)
            CalHisList.insert(0, f"sqr({number}) = {resultText}")
            self.UpdateHistoryList()
            return

        # SQUARE ROOT
        if operation == "√x":
            if current_number < 0:
                self.CalTxt.setText("Error")
                return

            result = current_number ** 0.5
            number = self.format_number(current_number)
            resultText = self.format_number(result)
            self.calTrackerLbl.setText(f"√({number})")
            self.calTrackerLbl.show()
            self.CalTxt.setText(resultText)
            CalHisList.insert(0, f"√({number}) = {resultText}")
            self.UpdateHistoryList()
            return

        # PI
        if operation == "π":
            result = self.format_number(math.pi)
            self.CalTxt.setText(result)
            return

        # E
        if operation == "e":
            result = self.format_number(math.e)
            self.CalTxt.setText(result)
            return

        # EQUALS
        if operation == "=":
            if (self.Num1 is None or self.Operator is None):
                return

            self.Num2 = current_number
            result = self.calculate(self.Num1, self.Operator, self.Num2)

            if result is None:
                self.CalTxt.setText("Error")
                self.Num1 = None
                self.Num2 = None
                self.Operator = None
                self.waiting_for_num2 = False
                return
            
            num1 = self.format_number(self.Num1)
            num2 = self.format_number(self.Num2)
            resultText = self.format_number(result)
            self.calTrackerLbl.setText(f"{num1} {self.Operator} {num2}")
            self.CalTxt.setText(resultText)
            CalHisList.insert(0, f"{num1} {self.Operator} " f"{num2} = {resultText}")
            self.UpdateHistoryList()
            self.Num1 = result
            self.Num2 = None
            self.Operator = None
            self.waiting_for_num2 = True
            return

        # BASIC OPERATORS
        if operation in ("+", "−", "×", "÷" ):
            if (self.Num1 is not None and self.Operator is not None):
                self.Num2 = current_number
                result = self.calculate(self.Num1, self.Operator, self.Num2)

                if result is None:
                    self.CalTxt.setText("Error")
                    self.Num1 = None
                    self.Num2 = None
                    self.Operator = None
                    self.waiting_for_num2 = False
                    return

                num1 = self.format_number(self.Num1)
                num2 = self.format_number(self.Num2)
                resultText = self.format_number(result)
                CalHisList.insert(0, f"{num1} {self.Operator} " f"{num2} = {resultText}")
                self.UpdateHistoryList()
                self.Num1 = result
                self.CalTxt.setText(resultText)
            else:
                self.Num1 = current_number
            
            self.Operator = operation
            self.waiting_for_num2 = True
            self.calTrackerLbl.setText(f"{self.format_number(self.Num1)} " f"{operation}")
            self.calTrackerLbl.show()

    def add_open_bracket(self):
        current = self.CalTxt.text()
        self.using_expression = True

        # Starting a new expression
        if (current == "0" or self.waiting_for_num2):
            self.expression = "("
            self.CalTxt.setText(self.expression)
            self.waiting_for_num2 = False
            self.bracket_count += 1
            return

        if (current[-1].isdigit() or current[-1] == ")"):
            self.expression += "×("
        else:
            self.expression += "("

        self.CalTxt.setText(self.expression)
        self.bracket_count += 1

    def add_close_bracket(self):
        if self.bracket_count <= 0:
            return

        if not self.expression:
            return

        # Don't allow: (+-x / sign
        if self.expression.endswith(
            ("(", "+", "−", "×", "÷")):
            return

        self.expression += ")"

        self.CalTxt.setText(self.expression)

        self.bracket_count -= 1

    # CALCULATE EXPRESSION
    def calculate_expression(self):
        expression = self.expression

        # Make sure every bracket is closed
        if self.bracket_count != 0:
            self.CalTxt.setText("Error")
            return

        # Convert calculator operators to Python
        python_expression = (expression.replace("×", "*").replace("÷", "/").replace("−", "-"))

        # Safety check
        allowed_characters = ("0123456789" ".+-*/() ")

        if not all(char in allowed_characters for char in python_expression):
            self.CalTxt.setText("Error")
            return

        # Evaluate
        #There is a line that uses the eval function, which might become a security problem 
        #So fix that when you finish the others
        try:
            result = eval(python_expression,{"__builtins__": None},{})

            # Prevent invalid result
            if not math.isfinite(result):
                raise ValueError
        except Exception:
            self.CalTxt.setText("Error")
            self.expression = ""
            self.bracket_count = 0
            self.using_expression = False
            return

        # Format result
        resultText = self.format_number(result)

        # Tracker
        self.calTrackerLbl.setText(f"{self.expression} =")
        self.calTrackerLbl.show()

        # Display result
        self.CalTxt.setText(resultText)
        # History
        CalHisList.insert(0,f"{self.expression} = {resultText}")

        self.UpdateHistoryList()

        # Prepare the variables for the next calculation
        self.expression = resultText
        self.bracket_count = 0
        self.using_expression = False
        self.Num1 = result
        self.Num2 = None
        self.Operator = None
        self.waiting_for_num2 = True

    #Perform the calculation based on the operator
    def calculate(self, num1, operator, num2):
        if operator == "+":
            return num1 + num2
        if operator == "−":
            return num1 - num2
        if operator == "×":
            return num1 * num2
        if operator == "÷":
            return None if num2 == 0 else num1 / num2
        return None

    #Format the calculation to make it easier to display on the history panel
    def format_number(self, number):
        return str(int(number)) if number == int(number) else str(number)

    #To toggle the history panel when the button is clicked
    def toggle_history_panel(self):
        self.historyPanel.setVisible(not self.historyPanel.isVisible())

    #When the user performs a calculation, inform the Listbox for the updates CalHisList
    def UpdateHistoryList(self):
        self.historyList.clear()
        self.historyList.addItems(CalHisList)

    #To clear the history on the Listbox
    def clear_history(self):
        CalHisList.clear()
        self.historyList.clear()

    #When double clicking an item on the Listbox, Display the item on the label and the Textbox
    def get_cal_item(self, item):
        text = item.text()
        #Split the text based on the placement of the = sign
        if "=" in text:
            result = text.split("=")[-1].strip()
            self.CalTxt.setText(result)
            self.Num1 = None
            self.Num2 = None
            self.Operator = None
            self.waiting_for_num2 = False
            self.CalTxt.setFocus()

    #To copy the selected item to the clipborad
    def copy_history_item(self):
        item = self.historyList.currentItem()

        if item:
            QtWidgets.QApplication.clipboard().setText(item.text())

    #To delete the selected item from the Listbox
    def delete_selected_history_item(self):
        item = self.historyList.currentItem()

        if item:
            self.delete_history_item(item)

    #To show the contextmenu for the listbox when an item is selected
    def show_history_context_menu(self, position):
        item = self.historyList.itemAt(position)

        if item is None:
            return

        self.historyList.setCurrentItem(item)

        menu = QtWidgets.QMenu(self.historyList)
        menu.addAction(self.copyAction)
        menu.addAction(self.deleteAction)
        menu.exec(self.historyList.viewport().mapToGlobal(position))

    def delete_history_item(self, item):
        row = self.historyList.row(item)

        if row >= 0:
            self.historyList.takeItem(row)

            if row < len(CalHisList):
                del CalHisList[row]