from PySide6 import QtGui, QtWidgets, QtCore
from PySide6.QtWidgets import QMessageBox
import qtawesome as qta
import requests
from countryinfo import all_countries
import socket

countries = all_countries()

class CurrencyCalculator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.converting = False
        self.currentInput = None  # Track which input is being edited

        # Network information
        self.networkWarningShown = False
        self.networkStatus = False

        # To and From variables
        self.fromCurrency = ""
        self.toCurrency = ""

        self.setMinimumWidth(380)

        MainLayout = QtWidgets.QVBoxLayout(self)
        MainLayout.setContentsMargins(10, 10, 10, 10)

        TopRow = QtWidgets.QHBoxLayout()

        # Fonts
        inputFont = QtGui.QFont("Arial", 18)
        comboFont = QtGui.QFont("Arial", 13)
        buttonFont = QtGui.QFont("Arial", 15)

        # Title
        self.Lbl = QtWidgets.QLabel("Currency")
        titleFont = QtGui.QFont("Arial", 14)
        titleFont.setBold(True)
        self.Lbl.setFont(titleFont)

        self.toggleBtn = QtWidgets.QCheckBox("Show buttons")
        self.toggleBtn.setToolTip("Show buttons (Ctrl+I)")
        self.toggleBtn.toggled.connect(self.showButtons)

        # Keyboard shortcut
        self.toggleShrtcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+I"), self)
        self.toggleShrtcut.activated.connect(self.toggleBtn.toggle)

        self.infoBtn = QtWidgets.QPushButton()
        self.infoBtn.setIcon(qta.icon("fa6s.info"))
        self.updateNetworkTooltip()

        validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"\d*\.?\d*"))

        # First input
        self.inputbox1 = QtWidgets.QLineEdit()
        self.inputbox1.setFixedHeight(55)
        self.inputbox1.setFont(inputFont)
        self.inputbox1.setValidator(validator)
        self.inputbox1.setText("1")
        self.inputbox1.setEnabled(False)
        self.inputbox1.textChanged.connect(self.setInput)
        self.inputbox1.focusInEvent = self.createFocusHandler(self.inputbox1, self.inputbox1.focusInEvent)

        # First combo
        self.combo1 = QtWidgets.QComboBox()
        self.combo1.setFont(comboFont)
        self.combo1.setMinimumHeight(40)
        self.combo1.setEnabled(False)
        self.combo1.currentTextChanged.connect(lambda text: self.getCurrency(text, "from"))
        self.combo1.currentTextChanged.connect(self.convertCurrencies)

        # Swap button
        self.swapButton = QtWidgets.QPushButton()
        self.swapButton.setFixedSize(35, 35)
        self.swapButton.setIcon(qta.icon("fa5s.exchange-alt"))
        self.swapButton.setIconSize(QtCore.QSize(15, 15))
        self.swapButton.setToolTip("Swap units (Ctrl+U)")
        self.swapButton.setEnabled(False)
        self.swapButton.clicked.connect(self.swapUnits)

        # Keyboard shortcut
        self.swapShtcut = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+U"), self)
        self.swapShtcut.activated.connect(self.swapUnits)

        # Second input
        self.inputbox2 = QtWidgets.QLineEdit()
        self.inputbox2.setFixedHeight(55)
        self.inputbox2.setFont(inputFont)
        self.inputbox2.setValidator(validator)
        self.inputbox2.setText("0")
        self.inputbox2.setEnabled(False)
        self.inputbox2.focusInEvent = self.createFocusHandler(self.inputbox2, self.inputbox2.focusInEvent)

        # Second combo
        self.combo2 = QtWidgets.QComboBox()
        self.combo2.setFont(comboFont)
        self.combo2.setMinimumHeight(40)
        self.combo2.setEnabled(False)
        self.combo2.currentTextChanged.connect(lambda text: self.getCurrency(text, "to"))
        self.combo2.currentTextChanged.connect(self.convertCurrencies)

        for country in countries:
            currencies = country.currencies()
            if currencies:
                formatComboItem = f"{country.name()} ({currencies[0]})"
                self.combo1.addItem(formatComboItem)
                self.combo2.addItem(formatComboItem)

        # Display the current exchange rate
        self.unitLbl = QtWidgets.QLabel()
        self.unitLbl.setFont(QtGui.QFont("Arial", 12))
        self.unitLbl.setStyleSheet("color: gray;")
        self.updateUnitLabel()
        self.combo1.currentTextChanged.connect(self.updateUnitLabel)
        self.combo2.currentTextChanged.connect(self.updateUnitLabel)

        # Button grid
        self.buttonGridWidget = QtWidgets.QWidget()
        self.buttonGrid = QtWidgets.QGridLayout(self.buttonGridWidget)
        self.buttonGrid.setContentsMargins(0, 10, 0, 0)
        self.buttonGrid.setSpacing(5)

        buttons = [["CE", "backspace"], ["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], [".", "0"]]

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
                    if text.isdigit() or text == ".":
                        button.clicked.connect(lambda _, v=text: self.number_clicked(v))
                    else:
                        button.clicked.connect(lambda _, v=text: self.operation_clicked(v))

                self.buttonGrid.addWidget(button, row, col)

        self.buttonGridWidget.setVisible(False)

        # Layout
        TopRow.addWidget(self.Lbl)
        TopRow.addStretch()
        TopRow.addWidget(self.toggleBtn)
        TopRow.addWidget(self.infoBtn)

        MainLayout.addLayout(TopRow)
        MainLayout.addWidget(self.inputbox1)
        MainLayout.addWidget(self.combo1)

        SwapLayout = QtWidgets.QHBoxLayout()
        SwapLayout.addStretch()
        SwapLayout.addWidget(self.swapButton)
        SwapLayout.addStretch()

        MainLayout.addLayout(SwapLayout)
        MainLayout.addWidget(self.inputbox2)
        MainLayout.addWidget(self.combo2)
        MainLayout.addWidget(self.unitLbl)
        MainLayout.addWidget(self.buttonGridWidget)

        QtWidgets.QApplication.instance().installEventFilter(self)

        if self.combo1.count() > 0:
            self.getCurrency(self.combo1.currentText(), "from")

        if self.combo2.count() > 0:
            self.getCurrency(self.combo2.currentText(), "to")

        # Check the network every 3 seconds
        self.networkTimer = QtCore.QTimer(self)
        self.networkTimer.timeout.connect(self.Checknetwork)
        self.networkTimer.start(3000)

        self.Checknetwork()

        QtCore.QTimer.singleShot(0, self.convertCurrencies)

    # Get the currency code from the combo box
    def getCurrency(self, text, comboTag):
        if not text or "(" not in text:
            return

        currency = text.rsplit("(", 1)[1].replace(")", "").strip()

        if comboTag == "from":
            self.fromCurrency = currency
        elif comboTag == "to":
            self.toCurrency = currency

    def convertCurrencies(self):
        if self.converting:
            return

        if not self.fromCurrency or not self.toCurrency:
            return

        if not self.networkStatus:
            self.inputbox2.clear()
            return

        text = self.inputbox1.text().strip()

        if not text:
            amount = 0
        else:
            try:
                amount = float(text)
            except ValueError:
                return

        if self.fromCurrency == self.toCurrency:
            self.inputbox2.setText(self.format_number(amount))
            return

        url = f"https://api.frankfurter.dev/v2/rate/{self.fromCurrency}/{self.toCurrency}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            convertedAmount = amount * data["rate"]
            self.inputbox2.setText(self.format_number(convertedAmount))
        except requests.RequestException as error:
            print("API error:", error)
        except (KeyError, TypeError, ValueError) as error:
            print("Conversion error:", error)

    # Track which input has focus
    def createFocusHandler(self, lineEdit, originalFocusEvent):
        def focusEvent(event):
            self.currentInput = lineEdit
            originalFocusEvent(event)
        return focusEvent

    def showButtons(self, checked):
        self.buttonGridWidget.setVisible(checked)
        self.adjustSize()

    def swapUnits(self):
        if self.converting or not self.networkStatus:
            return

        self.converting = True

        try:
            unit1 = self.combo1.currentText()
            unit2 = self.combo2.currentText()
            value1 = self.inputbox1.text()
            value2 = self.inputbox2.text()

            index1 = self.combo1.findText(unit2)
            index2 = self.combo2.findText(unit1)

            if index1 >= 0:
                self.combo1.setCurrentIndex(index1)

            if index2 >= 0:
                self.combo2.setCurrentIndex(index2)

            self.inputbox1.setText(value2)
            self.inputbox2.setText(value1)
        finally:
            self.converting = False

        self.getCurrency(self.combo1.currentText(), "from")
        self.getCurrency(self.combo2.currentText(), "to")

        if self.currentInput == self.inputbox1:
            self.inputbox1.setFocus()
        else:
            self.inputbox2.setFocus()

        self.convertCurrencies()

    # Handle keyboard input for the calculator
    def eventFilter(self, obj, event):
        if event.type() != QtCore.QEvent.Type.KeyPress:
            return super().eventFilter(obj, event)

        key = event.key()
        text = event.text()
        modifiers = event.modifiers()

        if modifiers & (QtCore.Qt.KeyboardModifier.ControlModifier | QtCore.Qt.KeyboardModifier.AltModifier):
            return super().eventFilter(obj, event)

        if isinstance(obj, QtWidgets.QComboBox):
            return super().eventFilter(obj, event)

        if self.currentInput is None:
            self.currentInput = self.inputbox1

        if text.isdigit():
            self.number_clicked(text)
            self.currentInput.setFocus()
            return True

        if key == QtCore.Qt.Key.Key_Backspace:
            self.operation_clicked("backspace")
            self.currentInput.setFocus()
            return True

        if key == QtCore.Qt.Key.Key_Escape:
            self.operation_clicked("CE")
            self.currentInput.setFocus()
            return True

        return super().eventFilter(obj, event)

    # Format numbers without unnecessary zeros
    def format_number(self, value):
        if value != 0 and (abs(value) >= 1e12 or abs(value) < 1e-9):
            return f"{value:.10g}"

        text = f"{value:.10f}".rstrip("0").rstrip(".")

        if text == "-0":
            text = "0"

        return text

    def number_clicked(self, value):
        line_edit = self.currentInput

        if line_edit is None:
            line_edit = self.inputbox1
            self.currentInput = line_edit

        current = line_edit.text()

        if value == ".":
            if "." in current:
                return

            if current == "":
                line_edit.setText("0.")
                return

        if current == "0" and value != ".":
            line_edit.setText(value)
        else:
            line_edit.insert(value)

    def operation_clicked(self, value):
        lineEdit = self.currentInput

        if lineEdit is None:
            lineEdit = self.inputbox1
            self.currentInput = lineEdit

        if value == "backspace":
            current = lineEdit.text()

            if current in ("", "0"):
                lineEdit.setText("0")
                return

            lineEdit.backspace()

            if lineEdit.text() == "":
                lineEdit.setText("0")

            return

        if value == "CE":
            lineEdit.setText("0")
            return

    # Update the displayed exchange rate
    def updateUnitLabel(self):
        if not self.fromCurrency or not self.toCurrency:
            self.unitLbl.clear()
            return

        if not self.networkStatus:
            self.unitLbl.clear()
            return

        if self.fromCurrency == self.toCurrency:
            self.unitLbl.setText(f"1 {self.fromCurrency} = 1 {self.toCurrency}")
            return

        url = f"https://api.frankfurter.dev/v2/rate/{self.fromCurrency}/{self.toCurrency}"

        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            rate = data["rate"]
            self.unitLbl.setText(f"1 {self.fromCurrency} = {rate:.4f} {self.toCurrency}")
        except requests.RequestException as error:
            print("API error:", error)
            self.unitLbl.clear()
        except (KeyError, TypeError, ValueError) as error:
            print("Rate error:", error)
            self.unitLbl.clear()

    # Replace an empty input with zero
    def setInput(self, text):
        if self.converting:
            return

        if text == "":
            self.converting = True
            self.inputbox1.setText("0")
            self.inputbox1.setCursorPosition(1)
            self.converting = False
            self.convertCurrencies()
            return

        self.convertCurrencies()

    # Check whether the Frankfurter API is reachable
    def Checknetwork(self):
        try:
            socket.create_connection(("api.frankfurter.dev", 443), timeout=2)

            wasDisconnected = not self.networkStatus
            self.networkStatus = True

            self.inputbox1.setEnabled(True)
            self.combo1.setEnabled(True)
            self.swapButton.setEnabled(True)
            self.inputbox2.setEnabled(True)
            self.combo2.setEnabled(True)

            self.networkWarningShown = False
            self.updateNetworkTooltip()

            if wasDisconnected:
                self.updateUnitLabel()
                self.convertCurrencies()

            return True

        except OSError:
            wasConnected = self.networkStatus
            self.networkStatus = False

            self.inputbox1.setEnabled(False)
            self.combo1.setEnabled(False)
            self.swapButton.setEnabled(False)
            self.inputbox2.setEnabled(False)
            self.combo2.setEnabled(False)

            self.inputbox2.clear()
            self.unitLbl.clear()
            self.updateNetworkTooltip()

            if wasConnected and not self.networkWarningShown:
                QMessageBox.warning(self, "No Internet Connection", "An internet connection is required for currency conversion.")
                self.networkWarningShown = True

            return False

    def updateNetworkTooltip(self):
        if self.networkStatus:
            status = '<span style="color: green;">Connected</span>'
        else:
            status = '<span style="color: red;">Disconnected</span>'

        self.infoBtn.setToolTip(f"For up to date rates, ensure you have an internet connection.<br>Network connection: {status}")

    def closeEvent(self, event):
        if hasattr(self, "networkTimer"):
            self.networkTimer.stop()

        event.accept()