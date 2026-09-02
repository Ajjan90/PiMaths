#The scientific calculator's code uses the same code as the Standard calculator's code but with more features added

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QAction
import qtawesome as qta
import math

CalHisList = [] #to store the calculation into this List
CalMemList = [] #to store the resulted number into a memory

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

        # Trigonometry, Memory
        self.BtnDropRow = QtWidgets.QHBoxLayout()  # To hold the dropdown buttons

        # Trigonometry Button
        self.TriButton = QtWidgets.QPushButton("Trigonometry")
        self.TriMenu = QtWidgets.QMenu(self.TriButton)
        self.SinAction = QtGui.QAction("sin", self)
        self.CosAction = QtGui.QAction("cos", self)
        self.TanAction = QtGui.QAction("tan", self)
        self.SinInverseAction = QtGui.QAction("sin⁻¹", self)
        self.CosInverseAction = QtGui.QAction("cos⁻¹", self)
        self.TanInverseAction = QtGui.QAction("tan⁻¹", self)

        #Apply the trigger functions for each action item
        self.SinAction.triggered.connect(lambda: self.SinFunction())
        self.CosAction.triggered.connect(lambda: self.CosFunction())
        self.TanAction.triggered.connect(lambda: self.TanFunction())
        self.SinInverseAction.triggered.connect(lambda: self.SinInverseFunction())
        self.CosInverseAction.triggered.connect(lambda: self.CosInverseFunction())
        self.TanInverseAction.triggered.connect(lambda: self.TanInverseFunction())

        #Add actions to menu
        TriActions1 = [self.SinAction, self.CosAction, self.TanAction]
        for actions in TriActions1:
            self.TriMenu.addAction(actions)
        self.TriMenu.addSeparator()
        TriActions2 = [self.SinInverseAction, self.CosInverseAction, self.TanInverseAction]
        for actionss in TriActions2:
            self.TriMenu.addAction(actionss)

        # Attach menu to button
        self.TriButton.setMenu(self.TriMenu)

        # Memory Button
        self.MemButton = QtWidgets.QPushButton("Memory")
        self.MemMenu = QtWidgets.QMenu(self.MemButton)
        self.MemClrAction = QtGui.QAction("MC (Memory Clear)", self)
        self.MemClrAction.setShortcut("Ctrl+L")
        self.MemRecallAction = QtGui.QAction("MR (Memory Recall)", self)
        self.MemRecallAction.setShortcut("Ctrl+R")
        self.MemAddAction = QtGui.QAction("M+ (Memory Add)", self)
        self.MemAddAction.setShortcut("Ctrl+P")
        self.MemSubAction = QtGui.QAction("M- (Memory Subtract)", self)
        self.MemSubAction.setShortcut("Ctrl+Q")
        self.MemStrAction = QtGui.QAction("MS (Memory Store)", self)
        self.MemStrAction.setShortcut("Ctrl+M")

        #Add actions to menu
        MemAction = [self.MemClrAction, self.MemRecallAction, self.MemAddAction, self.MemSubAction, self.MemStrAction]
        for action in MemAction:
            self.MemMenu.addAction(action)

        #Apply trigger actions to the Memory actions
        self.MemClrAction.triggered.connect(lambda: self.clear_memory())
        self.MemRecallAction.triggered.connect(lambda: self.MemoryRecall())
        self.MemAddAction.triggered.connect(lambda: self.MemoryAdd())
        self.MemSubAction.triggered.connect(lambda: self.MemorySub())
        self.MemStrAction.triggered.connect(lambda: self.MemoryStore())

        #Attach menus to this button
        self.MemButton.setMenu(self.MemMenu)

        # Add the dropdown buttons into the row
        self.BtnDropRow.addWidget(self.TriButton)
        self.BtnDropRow.addWidget(self.MemButton)

        #The grid layout for the buttons
        buttonGrid = QtWidgets.QGridLayout()
        buttonFont = QtGui.QFont("Arial", 15)

        buttons = [
            ["x³", "π", "e", "(", ")"],
            ["³√x", "%", "CE", "C", "backspace"],
            ["n!", "1/x", "x²", "√x", "÷"],
            ["10^x", "7", "8", "9", "×"],
            ["Mod", "4", "5", "6", "−"],
            ["tau", "1", "2", "3", "+"],
            ["log", "±", "0", ".", "="]
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
        mainRow.addLayout(self.BtnDropRow)
        mainRow.addLayout(buttonGrid)

        layout.addLayout(topRow)
        layout.addLayout(mainRow)

        # SidePanel
        self.SidePanel = QtWidgets.QFrame()
        self.SidePanel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.SidePanel.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.SidePanel.setMinimumWidth(300)

        # Tab control
        self.tabControl = QtWidgets.QTabWidget()
        self.HisTab = QtWidgets.QWidget() #History tab
        self.MemTab = QtWidgets.QWidget() # Memory tab

        # Add tabs
        self.tabControl.addTab(self.HisTab, "History")
        self.tabControl.addTab(self.MemTab, "Memory")

        # History tab layout
        historyLayout = QtWidgets.QVBoxLayout(self.HisTab)

        # History top row
        historyTopRow = QtWidgets.QHBoxLayout()
        TitleFont = QtGui.QFont("Arial", 14)
        TitleFont.setBold(True)

        # History title
        historyTitle = QtWidgets.QLabel("History")
        historyTitle.setFont(TitleFont)

        # Clear history button
        self.DelBtn = QtWidgets.QPushButton()
        self.DelBtn.setIcon(qta.icon("fa5s.trash"))
        self.DelBtn.setIconSize(QtCore.QSize(15, 15))
        self.DelBtn.setToolTip("Clear All History")
        self.DelBtn.setFixedSize(40, 40)
        self.DelBtn.clicked.connect(self.clear_history)

        # History list
        self.historyList = QtWidgets.QListWidget()
        self.historyList.setFont(QtGui.QFont("Arial", 11))
        self.historyList.itemDoubleClicked.connect(self.get_cal_item) # Double-click history item

        # Context menu
        self.historyList.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.historyList.customContextMenuRequested.connect(self.show_history_context_menu)
        
        self.copyAction = QtGui.QAction("Copy", self) # Copy action
        self.copyAction.setShortcut(QtGui.QKeySequence.Copy)
        self.copyAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.copyAction.triggered.connect(self.copy_history_item)
        self.historyList.addAction(self.copyAction)

        self.deleteAction = QtGui.QAction("Delete", self) # Delete action
        self.deleteAction.setShortcut(QtGui.QKeySequence.Delete)
        self.deleteAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.deleteAction.triggered.connect(self.delete_selected_history_item)
        self.historyList.addAction(self.deleteAction)

        # Add widgets to History top row
        historyTopRow.addWidget(historyTitle)
        historyTopRow.addStretch()
        historyTopRow.addWidget(self.DelBtn)

        # Add History content to History tab
        historyLayout.addLayout(historyTopRow)
        historyLayout.addWidget(self.historyList)

        # Memory tab
        memoryLayout = QtWidgets.QVBoxLayout(self.MemTab)
        MemTopRow = QtWidgets.QHBoxLayout() #Memory Top Row        

        #Memory Title
        self.MemTitle = QtWidgets.QLabel("Memory")
        self.MemTitle.setFont(TitleFont)

        #Clear Memory Button
        ClearMemBtn = QtWidgets.QPushButton(self)
        ClearMemBtn.setIcon(qta.icon("fa5s.trash"))
        ClearMemBtn.setIconSize(QtCore.QSize(15, 15))
        ClearMemBtn.setToolTip("Clear All Memory")
        ClearMemBtn.setFixedSize(40, 40)
        ClearMemBtn.clicked.connect(lambda: self.clear_memory())

        #Memory Listbox
        self.MemList = QtWidgets.QListWidget(self)
        self.MemList.setFont(QtGui.QFont("Arial", 11))
        self.MemList.itemDoubleClicked.connect(self.get_Mem_Item)
        self.MemList.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.MemList.customContextMenuRequested.connect(self.showMemoryContextmenu)

        #Memory Add Action Menu
        self.AddMemAction = QtGui.QAction("Memory Add", self)
        self.AddMemAction.setShortcut("Ctrl+P")
        self.AddMemAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.AddMemAction.triggered.connect(lambda: self.MemBtnAdd())
        self.MemList.addAction(self.AddMemAction)

        #Memory Subtract Action Menu
        self.SubMemAction = QtGui.QAction("Memory Subtract", self)
        self.SubMemAction.setShortcut("Ctrl+M")
        self.SubMemAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.SubMemAction.triggered.connect(self.MemBtnSub)
        self.MemList.addAction(self.SubMemAction)

        # Memory Clear Action Menu
        self.ClearMemAction = QtGui.QAction("Memory Clear", self)
        self.ClearMemAction.setShortcut("Ctrl+L")
        self.ClearMemAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.ClearMemAction.triggered.connect(self.MemBtnClear)
        self.MemList.addAction(self.ClearMemAction)

        #Bottom Buttons layout
        BottomRow = QtWidgets.QHBoxLayout()
        BottomRow.alignment()

        #Memory add button
        self.MemaddBtn = QtWidgets.QPushButton("M+")
        self.MemaddBtn.setEnabled(False)
        self.MemaddBtn.setToolTip("Add Memory")
        self.MemaddBtn.setFixedSize(40, 40)
        self.MemaddBtn.clicked.connect(lambda: self.MemBtnAdd())

        #Memory subtract button
        self.MemSubBtn = QtWidgets.QPushButton("M-")
        self.MemSubBtn.setEnabled(False)
        self.MemSubBtn.setToolTip("Subtract Memory")
        self.MemSubBtn.setFixedSize(40, 40)
        self.MemSubBtn.clicked.connect(lambda: self.MemBtnSub())
        
        #Memory clear button
        self.MemClrBtn = QtWidgets.QPushButton("MC")
        self.MemClrBtn.setEnabled(False)
        self.MemClrBtn.setToolTip("CLear/Remove Memory")
        self.MemClrBtn.setFixedSize(40, 40)
        self.MemClrBtn.clicked.connect(lambda: self.MemBtnClear())

        BottomRow.addWidget(self.MemaddBtn)
        BottomRow.addWidget(self.MemSubBtn)
        BottomRow.addWidget(self.MemClrBtn)
        self.MemList.itemSelectionChanged.connect(lambda: self.updateBtnState())

        #Add the widgets to the MemTopRow (Title and the Clear Button)
        MemTopRow.addWidget(self.MemTitle)
        MemTopRow.addStretch()
        MemTopRow.addWidget(ClearMemBtn)

        #Add the widgets to the Memory Layout
        memoryLayout.addLayout(MemTopRow)
        memoryLayout.addWidget(self.MemList)
        memoryLayout.addLayout(BottomRow)

        # Put the TabWidget inside the History panel
        historyPanelLayout = QtWidgets.QVBoxLayout(self.SidePanel)
        historyPanelLayout.setContentsMargins(0, 0, 0, 0)
        historyPanelLayout.addWidget(self.tabControl)

        # Initially hide History panel
        self.SidePanel.hide()

        # Add calculator + history panel to main layout
        mainLayout.addLayout(layout, 3)
        mainLayout.addWidget(self.SidePanel, 1)

        # Event filter
        QtWidgets.QApplication.instance().installEventFilter(self)

    # Function to show a Error message without needing to repeat the same lines of code
    def show_error(self):
        self.CalTxt.setText("Error")
        self.calTrackerLbl.clear()
        self.calTrackerLbl.hide()

        self.Num1 = None
        self.Num2 = None
        self.Operator = None
        self.waiting_for_num2 = False

        self.expression = ""
        self.bracket_count = 0
        self.using_expression = False

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
                        current_number = (char + current_number)
                    else:
                        break
                if "." in current_number:
                    return

            if (self.expression and self.expression[-1] == ")"):
                self.expression += "×"

            self.expression += number
            self.CalTxt.setText(self.expression)
            return

        # Normal calculator mode
        if self.waiting_for_num2:
            self.CalTxt.setText(number)
            self.waiting_for_num2 = False
            return

        # Prevent multiple decimal points
        if number == "." and "." in current:
            return

        # Replace initial zero
        if current == "0" and number != ".":
            self.CalTxt.setText(number)
        else:
            self.CalTxt.setText(current + number)

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

        # Percentage
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

        #Square
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

        #Cube
        if operation == "x³":
            result = current_number ** 3
            number = self.format_number(current_number)
            resultText = self.format_number(result)
            self.calTrackerLbl.setText(f"Cube({number})")
            self.calTrackerLbl.show()
            self.CalTxt.setText(resultText)
            CalHisList.insert(0, f"Cube({number}) = {resultText}")
            self.UpdateHistoryList()
            return

        # Square Root
        if operation == "√x":
            if current_number < 0:
                self.show_error()
                return

            try:
                result = math.sqrt(current_number)
                numberText = self.format_number(current_number)
                resultText = self.format_number(result)
                self.CalTxt.setText(resultText)
                self.calTrackerLbl.setText(f"√({numberText})")
                self.calTrackerLbl.show()
                CalHisList.insert(0, f"√({numberText}) = {resultText}")
                self.UpdateHistoryList()
            except (ValueError, OverflowError):
                self.show_error()
            return
        
        # Cube Root
        if operation == "³√x":
            try:
                if current_number < 0:
                    result = -((-current_number) ** (1 / 3))
                else:
                    result = current_number ** (1 / 3)

                numberText = self.format_number(current_number)
                resultText = self.format_number(result)
                self.CalTxt.setText(resultText)
                self.calTrackerLbl.setText(f"³√({numberText})")
                self.calTrackerLbl.show()
                CalHisList.insert(0, f"³√({numberText}) = {resultText}")
                self.UpdateHistoryList()
            except (ValueError, OverflowError):
                self.show_error()
            return

        # Pi
        if operation == "π":
            result = self.format_number(math.pi)
            self.CalTxt.setText(result)
            return

        #tau
        if operation == "tau":
            result = self.format_number(math.tau)
            self.CalTxt.setText(result)
            return

        # E
        if operation == "e":
            result = self.format_number(math.e)
            self.CalTxt.setText(result)
            return

        #10^x
        if operation == "10^x":
            result = self.format_number(10 ** current_number)
            number = self.format_number(current_number)
            self.calTrackerLbl.setText(f"10^({self.format_number(number)})")
            self.calTrackerLbl.show()
            self.CalTxt.setText(result)
            CalHisList.insert(0, f"10^({self.format_number(number)}) = {self.format_number(result)}")
            self.UpdateHistoryList()
            return

        #Factorial
        if operation == "n!":
            if not current_number.is_integer() or current_number < 0:
                self.show_error()
                return

            try:
                number = int(current_number)
                result = math.factorial(number)
                resultText = self.format_number(result)
                self.CalTxt.setText(resultText)
                self.calTrackerLbl.setText(f"fact({number})")
                self.calTrackerLbl.show()
                CalHisList.insert(0, f"fact({number}) = {resultText}")
                self.UpdateHistoryList()
            except (ValueError, OverflowError):
                self.show_error()
            return

       # Modulo / Remainder
        if operation == "Mod":
            if self.Num1 is None:
                self.show_error()
                return

            try:
                number = current_number

                if number == 0:
                    self.show_error()
                    return

                firstNum = self.Num1
                result = math.fmod(firstNum, number)
                firstText = self.format_number(firstNum)
                numberText = self.format_number(number)
                resultText = self.format_number(result)
                self.CalTxt.setText(resultText)
                self.calTrackerLbl.setText(f"{firstText} MOD {numberText}")
                self.calTrackerLbl.show()
                CalHisList.insert(0, f"{firstText} MOD {numberText} = {resultText}")
                self.UpdateHistoryList()
            except (ValueError, TypeError, ZeroDivisionError, OverflowError):
                self.show_error()
            return

        # Logarithm
        if operation == "log":
            if current_number <= 0:
                self.show_error()
                return

            try:
                result = math.log10(current_number)
                numberText = self.format_number(current_number)
                resultText = self.format_number(result)
                self.CalTxt.setText(resultText)
                self.calTrackerLbl.setText(f"log10({numberText})")
                self.calTrackerLbl.show()
                CalHisList.insert(0, f"log10({numberText}) = {resultText}")
                self.UpdateHistoryList()
            except (ValueError, OverflowError):
                self.show_error()
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
        if self.expression.endswith(("(", "+", "−", "×", "÷")):
            return

        self.expression += ")"
        self.CalTxt.setText(self.expression)
        self.bracket_count -= 1

    def tokenize_expression(self, expression):
        tokens = []
        i = 0

        while i < len(expression):
            char = expression[i]

            # Ignore spaces
            if char.isspace():
                i += 1
                continue

            # Operators / brackets
            if char in "+−×÷()":
                tokens.append(char)
                i += 1
                continue

            # Number
            if char.isdigit() or char == ".":
                start = i
                decimal_count = 0

                while i < len(expression) and (
                    expression[i].isdigit() or expression[i] == "."
                ):
                    if expression[i] == ".":
                        decimal_count += 1

                        if decimal_count > 1:
                            raise ValueError("Invalid number")

                    i += 1

                number_text = expression[start:i]

                # "." by itself isn't a valid number
                if number_text == ".":
                    raise ValueError("Invalid number")

                tokens.append(float(number_text))
                continue

            # Anything else is invalid
            raise ValueError("Invalid character")

        return tokens
    def evaluate_expression(self, expression):
        tokens = self.tokenize_expression(expression)
        position = 0

        def current_token():
            if position < len(tokens):
                return tokens[position]
            return None

        def parse_expression():
            nonlocal position

            result = parse_term()

            while current_token() in ("+", "−"):
                operator = current_token()
                position += 1

                right = parse_term()

                if operator == "+":
                    result += right
                else:
                    result -= right

            return result

        def parse_term():
            nonlocal position

            result = parse_factor()

            while current_token() in ("×", "÷"):
                operator = current_token()
                position += 1

                right = parse_factor()

                if operator == "×":
                    result *= right

                elif operator == "÷":
                    if right == 0:
                        raise ZeroDivisionError

                    result /= right

            return result

        def parse_factor():
            nonlocal position

            token = current_token()

            # Unary plus
            if token == "+":
                position += 1
                return parse_factor()

            # Unary minus
            if token == "−":
                position += 1
                return -parse_factor()

            # Parentheses
            if token == "(":
                position += 1

                result = parse_expression()

                if current_token() != ")":
                    raise ValueError("Missing closing bracket")

                position += 1
                return result

            # Number
            if isinstance(token, float):
                position += 1
                return token

            raise ValueError("Invalid expression")

        result = parse_expression()

        # There shouldn't be anything left over
        if position != len(tokens):
            raise ValueError("Unexpected token")

        if not math.isfinite(result):
            raise ValueError("Invalid result")

        return result

    def calculate_expression(self):
        expression = self.expression

        # Make sure every bracket is closed
        if self.bracket_count != 0:
            self.CalTxt.setText("Error")
            return

        try:
            result = self.evaluate_expression(expression)

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
        CalHisList.insert(0, f"{self.expression} = {resultText}")
        self.UpdateHistoryList()

        # Prepare variables for next calculation
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
        try:
            number = float(number)

            if not math.isfinite(number):
                return "Error"

            if number.is_integer():
                return str(int(number))

            return str(number)
        except (ValueError, TypeError, OverflowError):
            return "Error"

    #To toggle the history panel when the button is clicked
    def toggle_history_panel(self):
        self.SidePanel.setVisible(not self.SidePanel.isVisible())

    #When the user performs a calculation, inform the Listbox for the updates CalHisList
    def UpdateHistoryList(self):
        self.historyList.clear()
        self.historyList.addItems(CalHisList)

    #When user adds an value or a calculated value to the Memory List, inform the CalMemList about the new value
    def UpdateMemList(self):
        self.MemList.clear()
        self.MemList.addItems([str(value) for value in CalMemList])

    #To clear the history on the Listbox
    def clear_history(self):
        CalHisList.clear()
        self.historyList.clear()

    #To clear the memory from the Listbox
    #This is also used for the Memory Clear (MC)
    def clear_memory(self):
        self.MemList.clear()
        CalMemList.clear()

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

    #When user double clicks on an item on the Listbox, Display that item on the Textbox
    def get_Mem_Item(self, item):
        text = item.text()
        self.CalTxt.setText(text)
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

    #To show the contextmenu for the Memory listbox when an item is selected
    def showMemoryContextmenu(self, position):
        item = self.MemList.itemAt(position)

        if item is None:
            return

        self.historyList.setCurrentItem(item)

        menu = QtWidgets.QMenu(self.MemList)
        menu.addAction(self.AddMemAction)
        menu.addAction(self.SubMemAction)
        menu.addAction(self.ClearMemAction)
        menu.exec(self.MemList.viewport().mapToGlobal(position))
        pass

    def delete_history_item(self, item):
        row = self.historyList.row(item)

        if row >= 0:
            self.historyList.takeItem(row)

            if row < len(CalHisList):
                del CalHisList[row]
    
    #Trigonometry functions sin,cos,tan, sin-1, cos-1 and tan-1
    def SinFunction(self):
        value = float(self.CalTxt.text())

        result = math.sin(math.radians(value))
        resultText = self.format_number(result)
        numberText = self.format_number(value)

        self.CalTxt.setText(resultText)
        self.calTrackerLbl.setText(f"sin({numberText})")
        self.calTrackerLbl.show()

        CalHisList.insert(0, f"sin({numberText}) = {resultText}")

    def CosFunction(self):
        value = float(self.CalTxt.text())
        result = math.cos(math.radians(value))
        resultText = self.format_number(result)
        numbertext = self.format_number(value)

        self.CalTxt.setText(resultText)
        self.calTrackerLbl.setText(f"cos({numbertext})")
        self.calTrackerLbl.show()

        CalHisList.insert(0, f"cos({numbertext}) = {resultText}")

    def TanFunction(self):
        value = float(self.CalTxt.text())
        result = math.tan(math.radians(value))
        resultText = self.format_number(result)
        numbertext = self.format_number(value)

        self.CalTxt.setText(resultText)
        self.calTrackerLbl.setText(f"tan({numbertext})")
        self.calTrackerLbl.show()

        CalHisList.insert(0, f"tan({numbertext}) = {resultText}")

    def SinInverseFunction(self):
        try:
            value = float(self.CalTxt.text())

            if value < -1 or value > 1:
                self.show_error()
                return

            result = math.degrees(math.asin(value))
            resultText = self.format_number(result)
            numberText = self.format_number(value)
            self.CalTxt.setText(resultText)
            self.calTrackerLbl.setText(f"sin⁻¹({numberText})")
            self.calTrackerLbl.show()
            CalHisList.insert(0, f"sin⁻¹({numberText}) = {resultText}")
            self.UpdateHistoryList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    def CosInverseFunction(self):
        try:
            value = float(self.CalTxt.text())

            if value < -1 or value > 1:
                self.show_error()
                return

            result = math.degrees(math.acos(value))
            resultText = self.format_number(result)
            numberText = self.format_number(value)
            self.CalTxt.setText(resultText)
            self.calTrackerLbl.setText(f"cos⁻¹({numberText})")
            self.calTrackerLbl.show()
            CalHisList.insert(0, f"cos⁻¹({numberText}) = {resultText}")
            self.UpdateHistoryList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    
    def TanInverseFunction(self):
        try:
            value = float(self.CalTxt.text())
            result = math.degrees(math.atan(value))
            resultText = self.format_number(result)
            numberText = self.format_number(value)
            self.CalTxt.setText(resultText)
            self.calTrackerLbl.setText(f"tan⁻¹({numberText})")
            self.calTrackerLbl.show()
            CalHisList.insert(0, f"tan⁻¹({numberText}) = {resultText}")
            self.UpdateHistoryList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    #The Memory functions
    # Memory Store
    def MemoryStore(self):
        try:
            value = float(self.CalTxt.text())

            if not math.isfinite(value):
                self.show_error()
                return

            CalMemList.insert(0, value)
            self.UpdateMemList()

        except (ValueError, TypeError, OverflowError):
            self.show_error()


    # Memory Add
    def MemoryAdd(self):
        try:
            if not CalMemList:
                CalMemList.insert(0, 0.0)

            memValue = float(CalMemList[0])
            num = float(self.CalTxt.text())

            if not math.isfinite(num):
                self.show_error()
                return

            result = memValue + num
            CalMemList.insert(0, result)
            self.UpdateMemList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()


    # Memory Subtract
    def MemorySub(self):
        try:
            if not CalMemList:
                CalMemList.insert(0, 0.0)

            memValue = float(CalMemList[0])
            num = float(self.CalTxt.text())

            if not math.isfinite(num):
                self.show_error()
                return

            result = num - memValue
            CalMemList.insert(0, result)
            self.UpdateMemList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    # Memory Recall
    def MemoryRecall(self):
        if not CalMemList:
            self.show_error()
            return

        try:
            value = float(CalMemList[0])
            self.CalTxt.setText(self.format_number(value))
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    # Enable or disable the memory buttons when an item is or isn't selected
    def updateBtnState(self):
        hasSelected = bool(self.MemList.selectedItems())

        for btn in (self.MemaddBtn, self.MemSubBtn, self.MemClrBtn):
            btn.setEnabled(hasSelected)

    #Memory Button clicked logic (similar to the other Memory functions but based on the listbox)
    #These functions will also be used on the contextmenu for the MemListbox
    #Memory Add Button Logic
    def MemBtnAdd(self):
        try:
            selected = self.MemList.selectedItems()

            if not selected:
                return
            
            item = float(selected[0].text())
            num = float(self.CalTxt.text())
            result = item + num
            CalMemList.insert(0, result)
            self.UpdateMemList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    #Memory Subtract Button Logic
    def MemBtnSub(self):
        try:
            selected = self.MemList.selectedItems()

            if not selected:
                return

            item = float(selected[0].text())
            num = float(self.CalTxt.text())
            result = item - num
            CalMemList.insert(0, result)
            self.UpdateMemList()
        except (ValueError, TypeError, OverflowError):
            self.show_error()

    #Memory Clear Button Logic
    def MemBtnClear(self):
        selected = self.MemList.selectedItems()

        if not selected:
            return

        row = self.MemList.row(selected[0])
        CalMemList.pop(row)
        self.UpdateMemList()