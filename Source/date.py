from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import qtawesome as qta
from datetime import date
from dateutil.relativedelta import relativedelta

class DateCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(380)

        MainLayout = QtWidgets.QVBoxLayout(self)
        MainLayout.setContentsMargins(10, 10, 10, 10)

        # Fonts
        self.dateFont = QtGui.QFont("Arial", 16) # Font type for the datetimepicker
        self.lblFont = QtGui.QFont("Arial", 12) # Font type for the labels

        self.headFont = QtGui.QFont("Arial", 13) # Font type for the header labels
        self.headFont.setBold(True) 

        # Title
        self.Lbl = QtWidgets.QLabel("Date Calculation")
        self.titleFont = QtGui.QFont("Arial", 14)
        self.titleFont.setBold(True)
        self.Lbl.setFont(self.titleFont)

        # Tab control
        self.tabControl = QtWidgets.QTabWidget()

        # First tab (Difference between days)
        self.DifferenceDate()

        # Second tab (Add and Subtract days)
        self.AddSubDate()

        # Add the tabs into the tabcontrol
        self.tabControl.addTab(self.betDayTab, qta.icon("fa5s.calendar-alt"), "Difference between days")
        self.tabControl.addTab(self.asDayTab, qta.icon("fa6s.plus-minus"), "Add or Subtract days")
        self.tabControl.setStyleSheet("""
                                        QTabBar::tab {
                                            min-height: 42px;
                                            max-height: 42px;
                                        }
                                    """) # Define a fixed height for the tabs

        # Layout
        MainLayout.addWidget(self.Lbl)
        MainLayout.addWidget(self.tabControl)

    # To create the Difference Date calculator for Tabpage1
    def DifferenceDate(self):
        # Tab layout
        self.betDayTab = QtWidgets.QWidget()
        self.betDayLayout = QtWidgets.QVBoxLayout(self.betDayTab)
        self.betDayLayout.setContentsMargins(10, 10, 10, 10)

        # Contents in the betDaytab
        # Top row for this tabpage
        self.TopRow = QtWidgets.QHBoxLayout()

        # Refresh button to reset the inputboxes
        self.refBtn = QtWidgets.QPushButton()
        self.refBtn.setIcon(qta.icon("msc.debug-restart"))
        self.refBtn.setToolTip("Refresh (Ctrl+R)")
        self.refBtn.setFixedSize(35, 35)
        self.refBtn.clicked.connect(lambda: refreshInputs())
        # Shortcut for the refresh button
        self.refShtcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self.betDayLayout)
        self.refShtcut.activated.connect(self.refBtn.click)

        # Start date label
        self.strLbl = QtWidgets.QLabel("Start Date")
        self.strLbl.setFont(self.lblFont)

        # Start datepicker
        self.strPicker = QtWidgets.QDateTimeEdit()
        self.strPicker.setFont(self.dateFont)
        self.strPicker.setDateTime(QDateTime.currentDateTime())
        self.strPicker.setCalendarPopup(True)
        self.strPicker.setDisplayFormat("dd MMMM yyyy")
        self.strPicker.dateChanged.connect(lambda: calculateDate())

        # End date label
        self.endLbl = QtWidgets.QLabel("End Date")
        self.endLbl.setFont(self.lblFont)

        # End datepicker
        self.endPicker = QtWidgets.QDateTimeEdit()
        self.endPicker.setFont(self.dateFont)
        self.endPicker.setDateTime(QDateTime.currentDateTime())
        self.endPicker.setCalendarPopup(True)
        self.endPicker.setDisplayFormat("dd MMMM yyyy")
        self.endPicker.dateChanged.connect(lambda: calculateDate())

        # Output labels
        # Header label
        self.diffHeader = QtWidgets.QLabel("Difference")
        self.diffHeader.setFont(self.headFont)

        # Total days label
        self.daysLbl = QtWidgets.QLabel("Same Date")
        self.daysLbl.setFont(self.lblFont)

        # Date details label
        self.detLbl = QtWidgets.QLabel("")
        self.detLbl.setFont(self.lblFont)
        self.detLbl.setStyleSheet("color: gray;")

        # Add the contents in the betDayTab
        #Top row
        self.TopRow.addStretch()
        self.TopRow.addWidget(self.refBtn)

        self.betDayLayout.addLayout(self.TopRow)
        self.betDayLayout.addWidget(self.strLbl)
        self.betDayLayout.addWidget(self.strPicker)
        self.betDayLayout.addSpacing(35)
        self.betDayLayout.addWidget(self.endLbl)
        self.betDayLayout.addWidget(self.endPicker)
        self.betDayLayout.addSpacing(25)
        self.betDayLayout.addWidget(self.diffHeader)
        self.betDayLayout.addWidget(self.daysLbl)
        self.betDayLayout.addWidget(self.detLbl)
        self.betDayLayout.addStretch()

        # Function to run the date difference calculations
        def calculateDate():
            start = self.strPicker.date().toPython() # Get the date data from the first date picker in python date format
            end = self.endPicker.date().toPython() # Get the date data from the second date picker in python date format
            result = 0
            difference = 0

            if end < start:
                result = start - end
                difference = relativedelta(start, end)
            else:
                result = end - start
                difference = relativedelta(end, start)

            # get the total number of days from the result varaible
            TotalDays = result.days

            self.daysLbl.setText(f"{TotalDays} days")

            if TotalDays == 0:
                self.dayLbl.setText("Same date")
                self.detLbl.setText("")
            elif TotalDays < 7:
                self.detLbl.setText(f"{TotalDays} Days")
            elif difference.years == 0 and difference.months == 0:
                weeks = TotalDays // 7
                remainingDays = TotalDays % 7
                self.detLbl.setText(f"{weeks} Weeks and {remainingDays} Days")
            elif difference.years == 0:
                weeks = difference.days // 7
                remainingDays = difference.days % 7
                self.detLbl.setText(f"{difference.months} Months, {weeks} Weeks and {remainingDays} Days")
            else:
                weeks = difference.days // 7
                remainingDays = difference.days % 7
                self.detLbl.setText(f"{difference.years} Years, {difference.months} Months, {weeks} Weeks and {remainingDays} Days")

        # Function to reset the datetimepicker and the labels to default as it was
        def refreshInputs():
            self.strPicker.setDateTime(QDateTime.currentDateTime())
            self.endPicker.setDateTime(QDateTime.currentDateTime())
            self.dayLbl.setText("Same date")
            self.detLbl.setText("")

    # To create the Add/Subtract dates calculator for Tabpage2
    def AddSubDate(self):
        # Tab layout
        self.asDayTab = QtWidgets.QWidget()
        self.asDayLayout = QtWidgets.QVBoxLayout(self.asDayTab)
        self.asDayLayout.setContentsMargins(10, 10, 10, 10)
        self.asDayLayout.setSpacing(12)

        # Refresh button to reset the inputboxes
        self.refBtn = QtWidgets.QPushButton()
        self.refBtn.setIcon(qta.icon("msc.debug-restart"))
        self.refBtn.setToolTip("Refresh (Ctrl+R)")
        self.refBtn.setFixedSize(35, 35)
        self.refBtn.clicked.connect(lambda: refreshInputs())
        # Shortcut for the refresh button
        self.refShtcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+R"), self.asDayLayout)
        self.refShtcut.activated.connect(lambda: refreshInputs)

        # Add / Subtract radio buttons
        self.radioLayout = QtWidgets.QHBoxLayout()
        self.radioLayout.setSpacing(20)

        # Add (+) radio button. Set to checked by default
        self.addRadio = QtWidgets.QRadioButton("Add (+)")
        self.addRadio.setFont(self.lblFont)
        self.addRadio.setChecked(True)
        self.addRadio.toggled.connect(lambda: DateCalculation())

        # Subtract (-) radio button
        self.subRadio = QtWidgets.QRadioButton("Subtract (-)")
        self.subRadio.setFont(self.lblFont)
        self.subRadio.toggled.connect(lambda: DateCalculation())

        # Add the radio buttons into the radioLayout
        self.radioLayout.addWidget(self.addRadio)
        self.radioLayout.addWidget(self.subRadio)
        self.radioLayout.addStretch()
        self.radioLayout.addWidget(self.refBtn)

        # From label
        self.fromLbl = QtWidgets.QLabel("From")
        self.fromLbl.setFont(self.lblFont)

        # From date picker
        self.fromPicker = QtWidgets.QDateTimeEdit()
        self.fromPicker.setFont(self.dateFont)
        self.fromPicker.setDateTime(QDateTime.currentDateTime())
        self.fromPicker.setCalendarPopup(True)
        self.fromPicker.setDisplayFormat("dd MMMM yyyy")
        self.fromPicker.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.fromPicker.dateChanged.connect(lambda: DateCalculation())

        # Day / Month / Year group
        self.numGroup = QtWidgets.QGroupBox("Day, Month and Year")
        self.numGroup.setFont(self.lblFont)

        self.numLayout = QtWidgets.QHBoxLayout(self.numGroup)
        self.numLayout.setContentsMargins(10, 10, 10, 10)
        self.numLayout.setSpacing(10)

        # Day
        self.dayLayout = QtWidgets.QVBoxLayout()

        self.dayLbl = QtWidgets.QLabel("Days")
        self.dayLbl.setFont(self.lblFont)

        self.dayNum = QtWidgets.QSpinBox()
        self.dayNum.setFont(self.dateFont)
        self.dayNum.setRange(0, 999)
        self.dayNum.setValue(0)
        self.dayNum.valueChanged.connect(lambda: DateCalculation())

        self.dayLayout.addWidget(self.dayLbl)
        self.dayLayout.addWidget(self.dayNum)

        # Month
        self.monthLayout = QtWidgets.QVBoxLayout()

        self.monthLbl = QtWidgets.QLabel("Months")
        self.monthLbl.setFont(self.lblFont)

        self.monthNum = QtWidgets.QSpinBox()
        self.monthNum.setFont(self.dateFont)
        self.monthNum.setRange(0, 999)
        self.monthNum.setValue(0)
        self.monthNum.valueChanged.connect(lambda: DateCalculation())

        self.monthLayout.addWidget(self.monthLbl)
        self.monthLayout.addWidget(self.monthNum)

        # Year
        self.yearLayout = QtWidgets.QVBoxLayout()

        self.yearLbl = QtWidgets.QLabel("Years")
        self.yearLbl.setFont(self.lblFont)

        self.yearNum = QtWidgets.QSpinBox()
        self.yearNum.setFont(self.dateFont)
        self.yearNum.setRange(0, 999)
        self.yearNum.setValue(0)
        self.yearNum.valueChanged.connect(lambda: DateCalculation())

        self.yearLayout.addWidget(self.yearLbl)
        self.yearLayout.addWidget(self.yearNum)

        # Add the three controls to the group
        self.numLayout.addLayout(self.dayLayout)
        self.numLayout.addLayout(self.monthLayout)
        self.numLayout.addLayout(self.yearLayout)

        # Output label for the calculated date
        self.outlbl = QtWidgets.QLabel("")
        self.outlbl.setFont(self.lblFont)

        # Add the contents in the asDayLayout
        self.asDayLayout.addLayout(self.radioLayout)
        self.asDayLayout.addSpacing(10)
        self.asDayLayout.addWidget(self.fromLbl)
        self.asDayLayout.addWidget(self.fromPicker)
        self.asDayLayout.addSpacing(15)
        self.asDayLayout.addWidget(self.numGroup)
        self.asDayLayout.addSpacing(15)
        self.asDayLayout.addWidget(self.outlbl)

        # Push everything toward the top
        self.asDayLayout.addStretch()

        def DateCalculation():
            fromDate = self.fromPicker.date().toPython() # Get the date data from the date picker in python date format

            day = self.dayNum.value() # Get the day value
            month = self.monthNum.value() # Get the month value
            year = self.yearNum.value() # Get the year value

            difference = relativedelta(years=year, months=month, days=day)

            if self.addRadio.isChecked():
                fullDate = fromDate + difference
            elif self.subRadio.isChecked():
                fullDate = fromDate - difference

            self.outlbl.setText(f"Date: {fullDate.strftime('%d %B %Y')}") 
            #%B displays the months by letters instead of numbers which makes it easier yo read

        # Function to reset the Datetimepicker and labels to default inputs
        def refreshInputs():
            self.fromPicker.setDateTime(QDateTime.currentDateTime())
            self.dayNum.setValue(0)
            self.monthNum.setValue(0)
            self.yearNum.setValue(0)
            self.outlbl.setText("")
