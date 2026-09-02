from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
import statistics as Stat

NumList = [] #to store the calculation into this List

class AverageCalculator(QtWidgets.QWidget):
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
        self.Lbl = QtWidgets.QLabel("Average")
        font = QtGui.QFont("Arial", 14)
        font.setBold(True)
        self.Lbl.setFont(font)

        #Button to toggle the history sidepanel
        self.HisBtn = QtWidgets.QPushButton()
        self.HisBtn.setIcon(qta.icon("fa5s.history"))
        self.HisBtn.setIconSize(QtCore.QSize(15, 15))
        self.HisBtn.setToolTip("History")
        self.HisBtn.setFixedSize(40, 40)
        self.HisBtn.clicked.connect(self.toggle_history_panel)

        #The Textbox to run and display calculations
        self.CalTxt = QtWidgets.QLineEdit("0")
        self.CalTxt.setFixedHeight(55)
        self.CalTxt.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.CalTxt.setFont(QtGui.QFont("Arial", 25))
        self.CalTxt.setReadOnly(True)

        #Small label underneath the textbox to display the calculations
        self.calTrackerLbl = QtWidgets.QLabel()
        self.calTrackerLbl.setFont(QtGui.QFont("Arial", 10))
        self.calTrackerLbl.setStyleSheet("color: gray;")
        self.calTrackerLbl.setVisible(False)

        #Mean, Mode, Median and Range labels
        lblGrid = QtWidgets.QGridLayout()
        lblGrid.setHorizontalSpacing(5)
        lblGrid.setVerticalSpacing(5)

        fontHeader = QtGui.QFont("Arial", 10)
        fontHeader.setBold(True)

        fontOut = QtGui.QFont("Arial", 10)

        #Headers
        MeanHeader = QtWidgets.QLabel("Mean:")
        ModeHeader = QtWidgets.QLabel("Mode:")
        MedianHeader = QtWidgets.QLabel("Median:")
        RangeHeader = QtWidgets.QLabel("Range:")

        #Output labels
        self.meanoutlbl = QtWidgets.QLabel("0")
        self.modeoutlbl = QtWidgets.QLabel("0")
        self.medianoutlbl = QtWidgets.QLabel("0")
        self.rangoutlbl = QtWidgets.QLabel("0")

        #Fonts
        for lbl in (MeanHeader, ModeHeader, MedianHeader, RangeHeader):
            lbl.setFont(fontHeader)

        for lbl in (self.meanoutlbl, self.modeoutlbl, self.medianoutlbl, self.rangoutlbl):
            lbl.setFont(fontOut)

        #Left align labels
        for lbl in (MeanHeader, ModeHeader, MedianHeader, RangeHeader, self.meanoutlbl, self.modeoutlbl, self.medianoutlbl, self.rangoutlbl):
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        #Add widgets
        lblGrid.addWidget(MeanHeader, 0, 0)
        lblGrid.addWidget(self.meanoutlbl, 0, 1)
        lblGrid.addWidget(ModeHeader, 1, 0)
        lblGrid.addWidget(self.modeoutlbl, 1, 1)
        lblGrid.addWidget(MedianHeader, 2, 0)
        lblGrid.addWidget(self.medianoutlbl, 2, 1)
        lblGrid.addWidget(RangeHeader, 3, 0)
        lblGrid.addWidget(self.rangoutlbl, 3, 1)

        #Keep columns compact
        lblGrid.setColumnStretch(0, 0)
        lblGrid.setColumnStretch(1, 0)

        #The grid layout for the buttons
        buttonGrid = QtWidgets.QGridLayout()
        buttonFont = QtGui.QFont("Arial", 15)

        buttons = [["CE", "C", "backspace"],
            ["7", "8", "9"],
            ["4", "5", "6"],
            ["1", "2", "3"],
            [".", "0", "+", "="]]

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
        mainRow.addLayout(lblGrid)
        mainRow.addLayout(buttonGrid)

        layout.addLayout(topRow)
        layout.addLayout(mainRow)

        #The History panel to display calculation history
        self.historyPanel = QtWidgets.QFrame()
        self.historyPanel.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.historyPanel.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.historyPanel.setMinimumWidth(300)

        historyLayout = QtWidgets.QVBoxLayout(self.historyPanel)
        historyTopRow = QtWidgets.QHBoxLayout()

        #The title for the history panel
        historyTitle = QtWidgets.QLabel("Values")
        historyFont = QtGui.QFont("Arial", 14)
        historyFont.setBold(True)
        historyTitle.setFont(historyFont)

        #To display the number of items added
        self.valCount = QtWidgets.QLabel("Values: 0")
        self.valCount.setFont(fontOut)

        #The button to clear all history
        self.DelBtn = QtWidgets.QPushButton()
        self.DelBtn.setIcon(qta.icon("fa5s.times"))
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
        historyTopRow.addStretch()
        historyTopRow.addWidget(self.DelBtn)
        historyLayout.addLayout(historyTopRow)
        historyLayout.addWidget(self.valCount)
        historyLayout.addWidget(self.historyList)

        self.historyPanel.hide()

        mainLayout.addLayout(layout, 3)
        mainLayout.addWidget(self.historyPanel, 1)

        QtWidgets.QApplication.instance().installEventFilter(self)

    #The function to run a keypress event
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
            self.clear_history()
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

            self.Num1 = result
            self.Num2 = None
            self.Operator = None
            self.waiting_for_num2 = True
            return

        if operation == "+":
            self.store_number(current_number)

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
        return None

    #Format the number to make it easier to display
    def format_number(self, number):
        return str(int(number)) if number == int(number) else str(number)

    #Store the current number in NumList
    def store_number(self, value):
        if value.is_integer():
            value = int(value)

        NumList.append(value)
        self.UpdateHistoryList()
        self.UpdateAverage()

    #To toggle the history panel when the button is clicked
    def toggle_history_panel(self):
        self.historyPanel.setVisible(not self.historyPanel.isVisible())

    #Update the history list
    def UpdateHistoryList(self):
        self.historyList.clear()

        for value in NumList:
            self.historyList.addItem(self.format_number(value))

        self.valCount.setText(f"Values: {len(NumList)}")

    #To clear the history on the Listbox
    def clear_history(self):
        NumList.clear()
        self.historyList.clear()
        self.valCount.setText("Values: 0")
        self.meanoutlbl.setText("0")
        self.modeoutlbl.setText("0")
        self.medianoutlbl.setText("0")
        self.rangoutlbl.setText("0")

    #When double clicking an item on the Listbox, display the item in the textbox
    def get_cal_item(self, item):
        text = item.text()
        self.CalTxt.setText(text)
        self.Num1 = None
        self.Num2 = None
        self.Operator = None
        self.waiting_for_num2 = False
        self.CalTxt.setFocus()

    #To copy the selected item to the clipboard
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

    #Delete an item from NumList and the Listbox
    def delete_history_item(self, item):
        row = self.historyList.row(item)

        if row < 0:
            return

        del NumList[row]
        self.historyList.takeItem(row)
        self.valCount.setText(f"Values: {len(NumList)}")
        self.UpdateAverage()

    #Update the output labels
    def UpdateAverage(self):
        if len(NumList) == 0:
            self.meanoutlbl.setText("0")
            self.modeoutlbl.setText("0")
            self.medianoutlbl.setText("0")
            self.rangoutlbl.setText("0")
            return

        meanVal = Stat.mean(NumList)
        medianVal = Stat.median(NumList)
        modeVal = Stat.mode(NumList)

        minRangeVal = min(NumList)
        maxRangeVal = max(NumList)

        self.meanoutlbl.setText(self.format_number(meanVal))
        self.modeoutlbl.setText(self.format_number(modeVal))
        self.medianoutlbl.setText(self.format_number(medianVal))
        self.rangoutlbl.setText(f"Smallest {self.format_number(minRangeVal)}, Largest: {self.format_number(maxRangeVal)}")