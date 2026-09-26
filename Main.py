from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLabel
import qtawesome as qta

from Source.standard import StandardCalculator
from Source.scientific import ScientificCalculator
from Source.average import AverageCalculator
from Source.paper import PaperCalculator

#Unit Conversions
from Source.area import AreaCalculator
from Source.currency import CurrencyCalculator
from Source.date import DateCalculator
from Source.data import DataCalculator
from Source.energy import EnergyCalculator

appName = "Calculator"

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(420, 450)
        self.setWindowTitle(appName)
        self.setWindowIcon(QtGui.QIcon("PiMaths1.ico"))

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
        
        self.AveView = QtGui.QAction("Average", self) #Average
        self.AveView.setIcon(qta.icon("fa5s.percentage"))
        self.AveView.setShortcut("Alt+2")
        
        self.PaperView = QtGui.QAction("Paper Mode", self) #Paper Mode
        self.PaperView.setIcon(qta.icon("fa5s.file"))
        self.PaperView.setShortcut("Alt+3")
        
        self.AreaView = QtGui.QAction("Area", self) #Area
        self.AreaView.setIcon(qta.icon("mdi.grid"))
        self.AreaView.setShortcut("Alt+4")

        self.CurrView = QtGui.QAction("Currency", self) #Currency
        self.CurrView.setIcon(qta.icon("fa5s.money-bill"))
        self.CurrView.setShortcut("Alt+5")
        
        self.DateView = QtGui.QAction("Date Calculation", self) #Date Calculation
        self.DateView.setIcon(qta.icon("fa5.calendar-alt"))
        self.DateView.setShortcut("Alt+6")
        
        self.DataView = QtGui.QAction("Data", self) #Data
        self.DataView.setIcon(qta.icon("fa6s.hard-drive"))
        self.DataView.setShortcut("Alt+7")

        self.EneView = QtGui.QAction("Energy", self) #Energy
        self.EneView.setIcon(qta.icon("fa6s.bolt"))
        self.EneView.setShortcut("Alt+8")
        
        self.LenView = QtGui.QAction("Length", self) #Length
        self.LenView.setIcon(qta.icon("fa6s.ruler-horizontal"))
        self.LenView.setShortcut("Alt+9")

        self.preView = QtGui.QAction("Pressure", self) #Pressure
        self.preView.setShortcut("Alt+Shift+1")

        self.powView = QtGui.QAction("Power", self) #Power
        self.powView.setShortcut("Alt+Shift+2") #fa6s.bolt-lightning

        self.speedView = QtGui.QAction("Speed", self) #Speed
        self.speedView.setShortcut("Alt+Shift+3") #mdi.speedometer-medium

        self.TemView = QtGui.QAction("Temperature", self) #Temperature
        self.TemView.setShortcut("Alt+Shift+4")
        
        self.TimeView = QtGui.QAction("Time", self) #Time
        self.TimeView.setShortcut("Alt+Shift+5")

        self.VolView = QtGui.QAction("Volume", self) #Volume
        self.VolView.setShortcut("Alt+Shift+6")

        #Help Menu dropdown and its submenus
        self.HelpMenu = QtWidgets.QMenu("Help", self)
        self.PerMenu = QtGui.QAction("Preferences", self) #Preferences/Settings
        self.AboutMenu = QtGui.QAction("About", self) #About

        #Edit menu and its menuitems
        #self.menu_Bar.addMenu(self.EditMenu)
        #edit_actions = [self.CopyAction, self.PasteAction, self.CutAction, self.SelectAction]
        #for action in edit_actions:
        #    self.EditMenu.addAction(action)

        #View menu and its menuitems
        self.menu_Bar.addMenu(self.ViewMenu)
        view_actions = [self.StnView, self.SciView, self.AveView, self.PaperView]
        for action in view_actions:
            self.ViewMenu.addAction(action)

        self.ViewMenu.addSeparator()
        view_actions = [self.AreaView, self.CurrView, self.DateView, self.DataView, self.EneView, self.LenView, self.preView, self.powView, self.speedView, self.TemView, self.TimeView, self.VolView]        
        for action in view_actions:
            self.ViewMenu.addAction(action)
            
        self.menu_Bar.addMenu(self.HelpMenu)
        self.HelpMenu.addAction(self.PerMenu)
        self.HelpMenu.addAction(self.AboutMenu)

        #Menubar
        #Ending of menubar

        self.calculators = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.calculators)

        # Menu connections
        self.StnView.triggered.connect(self.show_standard)
        self.SciView.triggered.connect(self.show_scientific)
        self.AveView.triggered.connect(self.show_average)
        self.PaperView.triggered.connect(self.show_paper)
        self.AreaView.triggered.connect(self.show_Area)
        self.CurrView.triggered.connect(self.show_Curren)
        self.DateView.triggered.connect(self.show_Date)
        self.DataView.triggered.connect(self.show_Data)
        self.EneView.triggered.connect(self.show_Energy)

        # Start with Standard
        self.show_standard()

    def ClearCurrentFrame(self):
        current = self.calculators.currentWidget()

        if current is not None:
            self.calculators.removeWidget(current)
            current.deleteLater()


    # Display Standard    
    def show_standard(self):
        self.ClearCurrentFrame()
        self.standard_calculator = StandardCalculator()
        self.calculators.addWidget(self.standard_calculator)
        self.calculators.setCurrentWidget(self.standard_calculator)
        self.adjustSize()

    # Display Scientific
    def show_scientific(self):
        self.ClearCurrentFrame()
        self.scientific_calculator = ScientificCalculator()
        self.calculators.addWidget(self.scientific_calculator)
        self.calculators.setCurrentWidget(self.scientific_calculator)
        self.adjustSize()

    # Display Average
    def show_average(self):
        self.ClearCurrentFrame()
        self.average_calculator = AverageCalculator()
        self.calculators.addWidget(self.average_calculator)
        self.calculators.setCurrentWidget(self.average_calculator)
        self.adjustSize()

    # Display Paper Mode
    def show_paper(self):
        self.ClearCurrentFrame()
        self.paper_calculator = PaperCalculator()
        self.calculators.addWidget(self.paper_calculator)
        self.calculators.setCurrentWidget(self.paper_calculator)
        self.paper_calculator.inputBox.setFocus()
        self.adjustSize()

    # Display Area Calculator
    def show_Area(self):
        self.ClearCurrentFrame()
        self.area_calculator = AreaCalculator()
        self.calculators.addWidget(self.area_calculator)
        self.calculators.setCurrentWidget(self.area_calculator)
        self.adjustSize()

    # Display Currency Calculator
    def show_Curren(self):
        self.ClearCurrentFrame()
        self.curren_calculator = CurrencyCalculator()
        self.calculators.addWidget(self.curren_calculator)
        self.calculators.setCurrentWidget(self.curren_calculator)
        self.adjustSize()

    # Display Date Calculator
    def show_Date(self):
        self.ClearCurrentFrame()
        self.date_calculator = DateCalculator()
        self.calculators.addWidget(self.date_calculator)
        self.calculators.setCurrentWidget(self.date_calculator)
        self.adjustSize()

    # Display Data Calculator
    def show_Data(self):
        self.ClearCurrentFrame()
        self.data_calculator = DataCalculator()
        self.calculators.addWidget(self.data_calculator)
        self.calculators.setCurrentWidget(self.data_calculator)
        self.adjustSize()

    # Display Energy Calculator
    def show_Energy(self):
        self.ClearCurrentFrame()
        self.ene_calculator = EnergyCalculator()
        self.calculators.addWidget(self.ene_calculator)
        self.calculators.setCurrentWidget(self.ene_calculator)
        self.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.setApplicationName(appName)
    #app.setWindowIcon(QtGui.QIcon("PiMaths.ico"))
    #window.setWindowIcon(QtGui.QIcon("PiMaths.ico"))
    window.show()
    app.exec()