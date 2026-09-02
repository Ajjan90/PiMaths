from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
import math

#to store the calculation into this List
CalHisList = []

class StandardCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.Num1 = None
        self.Operator = None
        self.Num2 = None
        self.waiting_for_num2 = False

        mainLayout = QtWidgets.QHBoxLayout(self) #This will hold the Main content layout and the History layout
        layout = QtWidgets.QVBoxLayout() #The layout for the Main Content
        topRow = QtWidgets.QHBoxLayout() #This is for the Top row like Label and Button
        mainRow = QtWidgets.QVBoxLayout() # For the textbox and the Button grid

        #The Title 
        self.Lbl = QtWidgets.QLabel("Standard")
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

        #The grid layout for the buttons
        buttonGrid = QtWidgets.QGridLayout()
        buttonFont = QtGui.QFont("Arial", 15)

        buttons = [
            ["%", "CE", "C", "backspace"],
            ["1/x", "x²", "√x", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
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
        mainRow.addLayout(buttonGrid)

        layout.addLayout(topRow)
        layout.addLayout(mainRow)

        #The History panel to display calculation history
        self.historyPanel = QtWidgets.QFrame()
        self.historyPanel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.historyPanel.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.historyPanel.setMinimumWidth(300)

        historyLayout = QtWidgets.QVBoxLayout(self.historyPanel)
        historyTopRow = QtWidgets.QHBoxLayout() #The toprow for the history panel

        #the title for the history panel
        historyTitle = QtWidgets.QLabel("History")
        historyFont = QtGui.QFont("Arial", 14)
        historyFont.setBold(True)
        historyTitle.setFont(historyFont)

        #The button to clear all history
        self.DelBtn = QtWidgets.QPushButton()
        self.DelBtn.setIcon(qta.icon("fa5s.trash")) #Set the icon as a trash icon
        self.DelBtn.setIconSize(QtCore.QSize(15, 15))
        self.DelBtn.setToolTip("Clear All")
        self.DelBtn.setFixedSize(40, 40)
        self.DelBtn.clicked.connect(self.clear_history)

        #Add the Listbox to display the items
        self.historyList = QtWidgets.QListWidget()
        self.historyList.setFont(QtGui.QFont("Arial", 11))
        #The double-click function to display on the textbox
        self.historyList.itemDoubleClicked.connect(self.get_cal_item)
        #Set up the contextmenu
        self.historyList.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.historyList.customContextMenuRequested.connect(self.show_history_context_menu)

        #Contextmenu Item 1: Copy
        self.copyAction = QtGui.QAction("Copy", self)
        self.copyAction.setShortcut(QtGui.QKeySequence.Copy)
        self.copyAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.copyAction.triggered.connect(self.copy_history_item)
        self.historyList.addAction(self.copyAction)

        #Contextmenu Item 2: Delete
        self.deleteAction = QtGui.QAction("Delete", self)
        self.deleteAction.setShortcut(QtGui.QKeySequence.Delete)
        self.deleteAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetShortcut)
        self.deleteAction.triggered.connect(self.delete_selected_history_item)
        self.historyList.addAction(self.deleteAction)

        historyTopRow.addWidget(historyTitle)
        historyTopRow.addWidget(self.DelBtn)
        historyLayout.addLayout(historyTopRow)
        historyLayout.addWidget(self.historyList)

        self.historyPanel.hide() #Set the visisblity to hidden

        mainLayout.addLayout(layout, 3)
        mainLayout.addWidget(self.historyPanel, 1)

        QtWidgets.QApplication.instance().installEventFilter(self)

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

    #For the buttons, define what is being clicked as an operator like +-*/= C CE and others
    def operation_clicked(self, operation):
        current_text = self.CalTxt.text()

        if operation == "C":
            self.Num1 = None
            self.Num2 = None
            self.Operator = None
            self.CalTxt.setText("0")
            self.calTrackerLbl.clear()
            self.calTrackerLbl.hide()
            self.waiting_for_num2 = False
            return

        if operation == "CE":
            self.CalTxt.setText("0")
            self.waiting_for_num2 = False
            return

        if operation == "backspace":
            if current_text == "Error":
                self.CalTxt.setText("0")
                return
            self.CalTxt.setText(current_text[:-1] if len(current_text) > 1 else "0")
            return

        try:
            current_number = float(current_text)
        except ValueError:
            self.CalTxt.setText("Error")
            return

        if operation == "±":
            current_number *= -1
            self.CalTxt.setText(self.format_number(current_number))
            return

        if operation == "%":
            result = current_number / 100
            self.CalTxt.setText(self.format_number(result))
            return

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

        if operation == "=":
            if self.Num1 is None or self.Operator is None:
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

            CalHisList.insert(0, f"{num1} {self.Operator} {num2} = {resultText}")
            self.UpdateHistoryList()

            self.Num1 = result
            self.Num2 = None
            self.Operator = None
            self.waiting_for_num2 = True
            return

        if operation in ("+", "−", "×", "÷"):
            if self.Num1 is not None and self.Operator is not None:
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

                CalHisList.insert(0, f"{num1} {self.Operator} {num2} = {resultText}")
                self.UpdateHistoryList()

                self.Num1 = result
                self.CalTxt.setText(resultText)
            else:
                self.Num1 = current_number

            self.Operator = operation
            self.waiting_for_num2 = True
            self.calTrackerLbl.setText(f"{self.format_number(self.Num1)} {operation}")
            self.calTrackerLbl.show()

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