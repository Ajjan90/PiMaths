from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLabel
import qtawesome as qta

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(340, 450)
        self.setWindowTitle("Calculator")

        #The MenuBar
        #The starting of the menubar
        self.menu_Bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menu_Bar)

        #Edit Menu dropdown and its submenus
        self.EditMenu = QtWidgets.QMenu("Edit", self)
        self.CopyAction = QtGui.QAction("Copy", self) #Copy
        self.CopyAction.setIcon(qta.icon("fa5s.copy"))
        self.CopyAction.setShortcut("Ctrl+C")
        
        self.PasteAction = QtGui.QAction("Paste", self) # Paste
        self.PasteAction.setIcon(qta.icon("fa5s.paste"))
        self.PasteAction.setShortcut("Ctrl+V")

        self.CutAction = QtGui.QAction("Cut", self) # Cut
        self.CutAction.setIcon(qta.icon("fa5s.cut"))
        self.CutAction.setShortcut("Ctrl+X")

        self.SelectAction = QtGui.QAction("Select All", self) #Select All
        self.SelectAction.setIcon(qta.icon("fa5s.border-all"))
        self.SelectAction.setShortcut("Ctrl+A")

        #View Menu dropdown and its submenus
        self.ViewMenu = QtWidgets.QMenu("View", self)
        self.StnView = QtGui.QAction("Standard", self) #Standard
        self.StnView.setIcon(qta.icon("fa5s.calculator"))
        self.StnView.setShortcut("Alt+0")
        
        self.SciView = QtGui.QAction("Scientific", self) #Scientific
        self.SciView.setIcon(qta.icon("fa5s.flask"))
        self.SciView.setShortcut("Alt+1")
        
        self.ProView = QtGui.QAction("Programmer", self) #Programming
        self.ProView.setIcon(qta.icon("fa5s.code"))
        self.ProView.setShortcut("Alt+2")
        
        self.PaperView = QtGui.QAction("Paper Mode", self) #Paper Mode
        self.PaperView.setIcon(qta.icon("fa5s.file"))
        self.PaperView.setShortcut("Alt+3")
        
        self.TemView = QtGui.QAction("Temperature", self) #Temperature
        self.TemView.setShortcut("Alt+4")
        
        self.VolView = QtGui.QAction("Volumne", self) #Volumne
        self.VolView.setShortcut("Alt+5")
        
        self.AreaView = QtGui.QAction("Area", self) #Area
        self.AreaView.setShortcut("Alt+6")
        
        self.LenView = QtGui.QAction("Length", self) #Length
        self.LenView.setShortcut("Alt+7")
        
        self.DateView = QtGui.QAction("Date Calculation", self) #Date Calculation
        self.DateView.setShortcut("Alt+8")
        
        self.TimeView = QtGui.QAction("Time", self) #Time
        self.TimeView.setShortcut("Alt+9")
        
        self.DataView = QtGui.QAction("Data", self) #Data
        self.DataView.setShortcut("Alt+Shift+1")
        
        self.CurrView = QtGui.QAction("Currency", self) #Currency
        self.CurrView.setShortcut("Alt+Shift+2")

        #Help Menu dropdown and its submenus
        self.HelpMenu = QtWidgets.QMenu("Help", self)
        self.PerMenu = QtGui.QAction("Perfernce", self) #Perfernce/Settings
        self.AboutMenu = QtGui.QAction("About", self) #About

        #Edit menu and its menuitems
        self.menu_Bar.addMenu(self.EditMenu)
        edit_actions = [self.CopyAction, self.PasteAction, self.CutAction, self.SelectAction]
        for action in edit_actions:
            self.EditMenu.addAction(action)

        #View menu and its menuitems
        self.menu_Bar.addMenu(self.ViewMenu)
        view_actions = [self.StnView, self.SciView, self.ProView, self.PaperView]
        for action in view_actions:
            self.ViewMenu.addAction(action)

        self.ViewMenu.addSeparator()
        view_actions = [self.TemView,self.VolView, self.AreaView, self.LenView, self.DateView, self.TimeView, self.DataView, self.CurrView]
        for action in view_actions:
            self.ViewMenu.addAction(action)
            
        self.menu_Bar.addMenu(self.HelpMenu)
        self.HelpMenu.addAction(self.PerMenu)
        self.HelpMenu.addAction(self.AboutMenu)

        #Menubar
        #Ending of menubar

        self.calculators = QtWidgets.QStackedWidget()

        self.standard_calculator = StandardCalculator()
        self.scientific_calculator = ScientificCalculator()

        self.calculators.addWidget(self.standard_calculator)
        self.calculators.addWidget(self.scientific_calculator)

        self.setCentralWidget(self.calculators)

        # Menu connections
        self.StnView.triggered.connect(self.show_standard)
        self.SciView.triggered.connect(self.show_scientific)

        # Start with Standard
        self.show_standard()

    def show_standard(self):
        self.calculators.setCurrentWidget(self.standard_calculator)

    def show_scientific(self):
        self.calculators.setCurrentWidget(self.scientific_calculator)

#The calculators and its other menus
class StandardCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        Num1 = "0"
        Operator = None
        Num2 = None


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
        validator = QtGui.QIntValidator(0, 999999)
        self.CalTxt.setValidator(validator)

        self.calTrackerLbl = QtWidgets.QLabel("0+0")
        smallLbl = QtGui.QFont("Arial", 10)
        self.calTrackerLbl.setStyleSheet("color: gray;")
        self.calTrackerLbl.setFont(smallLbl)
        self.calTrackerLbl.setVisible(False)

        ButtonGrid = QtWidgets.QGridLayout()

        ButtonGrid.addWidget(QtWidgets.QPushButton("%"), 0, 0)
        ButtonGrid.addWidget(QtWidgets.QPushButton("CE"), 0, 1)
        ButtonGrid.addWidget(QtWidgets.QPushButton("C"), 0, 2)

        delete_button = QtWidgets.QPushButton()
        delete_button.setIcon(qta.icon("fa5s.backspace"))
        delete_button.setIconSize(QtCore.QSize(10, 10))

        ButtonGrid = QtWidgets.QGridLayout()
        BtnFont = QtGui.QFont("Arial", 15)

        buttons = [
            ["%", "CE", "C", "backspace"],
            ["1/x", "x²", "√x", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="],
        ]

        for row, button_row in enumerate(buttons):
            for col, text in enumerate(button_row):

                button = QtWidgets.QPushButton()
                button.setFont(BtnFont)
                button.setFixedHeight(50)

                if text == "backspace":
                    button.setIcon(qta.icon("fa5s.backspace"))
                    button.setIconSize(QtCore.QSize(18, 18))
                    value = "backspace"
                    button.clicked.connect(
                        lambda _, v=value: self.operation_clicked(v)
                    )

                else:
                    button.setText(text)

                    if text.isdigit() or text == ".":
                        button.clicked.connect(
                            lambda _, v=text: self.number_clicked(v)
                        )
                    else:
                        button.clicked.connect(
                            lambda _, v=text: self.operation_clicked(v)
                        )

                ButtonGrid.addWidget(button, row, col)


            layout.addLayout(TopRow)
            layout.addLayout(MainRow)

            TopRow.addWidget(self.Lbl)
            TopRow.addWidget(self.HisBtn)
            MainRow.addWidget(self.CalTxt)
            MainRow.addWidget(self.calTrackerLbl, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
            layout.setAlignment(MainRow, QtCore.Qt.AlignmentFlag.AlignTop)
            layout.addLayout(ButtonGrid)

    def number_clicked(self, number):
        pass

    def operation_clicked(self, operation):
        pass

class ScientificCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        layout = QtWidgets.QVBoxLayout(self)

        self.display = QtWidgets.QLineEdit()
        layout.addWidget(self.display)

        # Your scientific calculator HisBtns go here
        layout.addWidget(QtWidgets.QPushButton("Scientific Calculator"))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
