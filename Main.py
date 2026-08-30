from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLabel
import qtawesome as qta

from Source.standard import StandardCalculator
from Source.scientific import ScientificCalculator

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(420, 450)
        self.setWindowTitle("Calculator")

        #The MenuBar
        #The starting of the menubar
        self.menu_Bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menu_Bar)

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
        #self.menu_Bar.addMenu(self.EditMenu)
        #edit_actions = [self.CopyAction, self.PasteAction, self.CutAction, self.SelectAction]
        #for action in edit_actions:
        #    self.EditMenu.addAction(action)

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


        self.setCentralWidget(self.calculators)

        # Menu connections
        self.StnView.triggered.connect(self.show_standard)
        self.SciView.triggered.connect(self.show_scientific)

        # Start with Standard
        self.show_standard()

    def ClearCurrentFrame(self):
        current = self.calculators.currentWidget()
        if current is not None:
            self.calculators.removeWidget(current)

    # Display Standard    
    def show_standard(self):
        self.ClearCurrentFrame()
        self.calculators.addWidget(self.standard_calculator)
        self.calculators.setCurrentWidget(self.standard_calculator)
        self.adjustSize()


    # Display Scientific
    def show_scientific(self):
        self.ClearCurrentFrame()
        self.calculators.addWidget(self.scientific_calculator)
        self.calculators.setCurrentWidget(self.scientific_calculator)
        self.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.show()

    app.exec()