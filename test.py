import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateTimeEdit
from PySide6.QtCore import QDateTime


app = QApplication(sys.argv)

window = QWidget()
layout = QVBoxLayout(window)

datetime_picker = QDateTimeEdit()
datetime_picker.setDateTime(QDateTime.currentDateTime())
datetime_picker.setCalendarPopup(True)
datetime_picker.setDisplayFormat("dd/MM/yyyy")

layout.addWidget(datetime_picker)

window.show()
sys.exit(app.exec())




#to store all the numbers or values that the user will input
NumList = []

 #Mean, Mode, Median and Range labels
        # Create grid
        lblGrid = QtWidgets.QGridLayout()

        # Reduce space between columns
        lblGrid.setHorizontalSpacing(5)
        lblGrid.setVerticalSpacing(5)

        fontHeader = QtGui.QFont("Arial", 10)
        fontHeader.setBold(True)

        fontOut = QtGui.QFont("Arial", 10) # set the outputs font type 

        # Headers
        MeanHeader = QtWidgets.QLabel("Mean:")
        ModeHeader = QtWidgets.QLabel("Mode:")
        MedianHeader = QtWidgets.QLabel("Median:")
        RangeHeader = QtWidgets.QLabel("Range:")

        # Output labels
        self.meanoutlbl = QtWidgets.QLabel("0")
        self.modeoutlbl = QtWidgets.QLabel("0")
        self.medianoutlbl = QtWidgets.QLabel("0")
        self.rangoutlbl = QtWidgets.QLabel("0")

# Fonts
        for lbl in (MeanHeader, ModeHeader, MedianHeader, RangeHeader):
            lbl.setFont(fontHeader)

        for lbl in (self.meanoutlbl, self.modeoutlbl, self.medianoutlbl, self.rangoutlbl):
            lbl.setFont(fontOut)

        # Left align labels
        for lbl in (MeanHeader, ModeHeader, MedianHeader, RangeHeader, self.meanoutlbl, self.modeoutlbl, self.medianoutlbl, self.rangoutlbl):
            lbl.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        # Add widgets
        lblGrid.addWidget(MeanHeader,   0, 0)
        lblGrid.addWidget(self.meanoutlbl,   0, 1)

        lblGrid.addWidget(ModeHeader,   1, 0)
        lblGrid.addWidget(self.modeoutlbl,   1, 1)

        lblGrid.addWidget(MedianHeader, 2, 0)
        lblGrid.addWidget(self.medianoutlbl, 2, 1)

        lblGrid.addWidget(RangeHeader,  3, 0)
        lblGrid.addWidget(self.rangoutlbl,   3, 1)

        # Keep columns compact
        lblGrid.setColumnStretch(0, 0)
        lblGrid.setColumnStretch(1, 0)

def StoreCurrentNum(self):
        try:
            value = float(self.CalTxt.text())

            if value.is_integer():
                value = int(value)

            NumList.append(value)

        except ValueError:
            pass

    #To clear the NumList and reset the output labels to 0
    def clearList(self, defaultValue):
        if len(NumList) > 0:
            NumList.clear()
            self.meanoutlbl.setText(defaultValue)
            self.medianoutlbl.setText(defaultValue)
            self.modeoutlbl.setText(defaultValue)
            self.rangoutlbl.setText(defaultValue)
        else:
            return

    #Update the output labels
    def UpdateAverage(self):
        if len(NumList) > 0:
            meanVal = statistics.mean(NumList)
            modeVal = statistics.mode(NumList)
            medianVal = statistics.median(NumList)

            #Get the range of the list
            minRangeVal = min(NumList)
            maxRangeVal = max(NumList)

            #Apply the data into the output labels
            self.meanoutlbl.setText(str(meanVal))
            self.modeoutlbl.setText(str(modeVal))
            self.medianoutlbl.setText(str(medianVal))
            self.rangoutlbl.setText(f"Smallest {str(minRangeVal)}, Largest: {str(maxRangeVal)}")