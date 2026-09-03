from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QLabel
import qtawesome as qta

class PaperCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QtWidgets.QHBoxLayout(self) #This will hold the Main content layout and the History layout
        layout = QtWidgets.QVBoxLayout() #The layout for the Main Content
        topRow = QtWidgets.QHBoxLayout() #This is for the Top row like Label and Button
        mainRow = QtWidgets.QVBoxLayout() # For the textbox and the Button grid

        #The Title 
        self.Lbl = QtWidgets.QLabel("Scientific")
        font = QtGui.QFont("Arial", 14)
        font.setBold(True)
        self.Lbl.setFont(font)

        mainLayout.addWidget(self.Lbl)