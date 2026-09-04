from PySide6 import QtWidgets, QtCore

class HelpWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Paper Mode Help")
        self.resize(520, 650)
        self.setMinimumSize(450, 550)

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QtWidgets.QVBoxLayout(centralWidget)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # Header
        header = QtWidgets.QFrame()
        header.setObjectName("header")

        headerLayout = QtWidgets.QVBoxLayout(header)
        headerLayout.setContentsMargins(25, 25, 25, 22)
        headerLayout.setSpacing(5)

        title = QtWidgets.QLabel("Paper Mode")
        title.setObjectName("title")

        subtitle = QtWidgets.QLabel("Learn how to use Paper Mode and its features.")
        subtitle.setObjectName("subtitle")

        headerLayout.addWidget(title)
        headerLayout.addWidget(subtitle)

        mainLayout.addWidget(header)

        # Scroll Area
        scrollArea = QtWidgets.QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        contentWidget = QtWidgets.QWidget()

        contentLayout = QtWidgets.QVBoxLayout(contentWidget)
        contentLayout.setContentsMargins(25, 25, 25, 25)
        contentLayout.setSpacing(18)

        scrollArea.setWidget(contentWidget)

        mainLayout.addWidget(scrollArea)

        # Getting Started
        gettingStarted = self.createCard(
            "Getting Started",
            "Enter a calculation in the input box and press "
            "Enter or click the <b>=</b> button."
        )

        contentLayout.addWidget(gettingStarted)

        # Basic Calculations
        basicCard = self.createCardWidget()

        basicLayout = basicCard.layout()

        basicTitle = self.createSectionTitle("Basic Calculations")

        basicLayout.addWidget(basicTitle)

        calculations = [
            ("Addition", "2 + 3", "5"),
            ("Subtraction", "5 - 2", "3"),
            ("Multiplication", "4 * 5", "20"),
            ("Division", "10 / 2", "5"),
            ("Power", "2 ** 3", "8"),
        ]

        for name, expression, result in calculations:
            row = self.createCalculationRow(
                name,
                expression,
                result
            )

            basicLayout.addWidget(row)

        contentLayout.addWidget(basicCard)

        # Parentheses
        parenthesesCard = self.createCard(
            "Parentheses",
            "Use parentheses to control the order of "
            "calculations.<br><br>"
            "<b>Example</b><br>"
            "<b>2 * (3 + 4)</b> &nbsp; → &nbsp; 14<br>"
            "<b>(10 + 2) / 4</b> &nbsp; → &nbsp; 3"
        )

        contentLayout.addWidget(parenthesesCard)

        # Paper Mode
        paperCard = self.createCardWidget()

        paperLayout = paperCard.layout()

        paperTitle = self.createSectionTitle("Paper Mode")

        paperLayout.addWidget(paperTitle)

        paperDescription = QtWidgets.QLabel(
            "Paper Mode keeps your calculations visible "
            "so you can review your previous work."
        )

        paperDescription.setObjectName("cardText")
        paperDescription.setWordWrap(True)

        paperLayout.addWidget(paperDescription)

        example = QtWidgets.QLabel(
            "25 * 4<br>"
            "<span>= 100</span><br><br>"
            "100 / 5<br>"
            "<span>= 20</span>"
        )

        example.setObjectName("example")
        example.setTextFormat(
            QtCore.Qt.TextFormat.RichText
        )

        paperLayout.addWidget(example)

        contentLayout.addWidget(paperCard)

        # Keyboard Shortcuts
        shortcutCard = self.createCardWidget()

        shortcutLayout = shortcutCard.layout()

        shortcutTitle = self.createSectionTitle("Keyboard Shortcuts")

        shortcutLayout.addWidget(shortcutTitle)

        shortcuts = [
            ("Enter", "Calculate"),
            ("Ctrl + Space", "Clear paper"),
            ("Ctrl + Shift + C", "Copy all"),
        ]

        for shortcut, action in shortcuts:
            row = self.createShortcutRow(
                shortcut,
                action
            )

            shortcutLayout.addWidget(row)

        contentLayout.addWidget(shortcutCard)

        # Spacer
        contentLayout.addStretch()

        # Bottom Button
        bottomFrame = QtWidgets.QFrame()
        bottomFrame.setObjectName("bottomFrame")

        bottomLayout = QtWidgets.QHBoxLayout(bottomFrame)
        bottomLayout.setContentsMargins(25, 12, 25, 18)
        bottomLayout.addStretch()

        closeButton = QtWidgets.QPushButton("Close")
        closeButton.setObjectName("closeButton")
        closeButton.setFixedSize(90, 36)
        closeButton.clicked.connect(self.close)

        bottomLayout.addWidget(closeButton)

        mainLayout.addWidget(bottomFrame)

        # Theme-aware styling
        self.setStyleSheet("""
            /* =====================================
            Header
            ===================================== */

            #header {
                border-bottom: 1px solid palette(midlight);
            }

            #title {
                font-size: 24px;
                font-weight: 700;
            }

            #subtitle {
                font-size: 13px;
                color: palette(text);
            }


            /* =====================================
            Scroll Area
            ===================================== */

            QScrollArea {
                border: none;
            }

            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 4px;
            }

            QScrollBar::handle:vertical {
                background: palette(mid);
                border-radius: 4px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover {
                background: palette(dark);
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }


            /* =====================================
            Cards
            ===================================== */

            #card {
                border: 1px solid palette(midlight);
                border-radius: 12px;
            }

            #sectionTitle {
                font-size: 15px;
                font-weight: 700;
            }

            #cardText {
                font-size: 13px;
                color: palette(text);
            }


            /* =====================================
            Calculation Rows
            ===================================== */

            #calculationRow {
                border: 1px solid palette(midlight);
                border-radius: 8px;
            }

            #calculationName {
                font-size: 12px;
                color: palette(text);
            }

            #calculationExpression {
                font-size: 13px;
                font-family: Consolas;
            }

            #calculationResult {
                font-size: 13px;
                font-weight: 700;
                font-family: Consolas;
            }


            /* =====================================
            Example
            ===================================== */

            #example {
                border: 1px solid palette(midlight);
                border-radius: 8px;
                padding: 12px;
                font-family: Consolas;
                font-size: 13px;
            }


            /* =====================================
            Shortcut Keys
            ===================================== */

            #shortcutKey {
                border: 1px solid palette(midlight);
                border-radius: 6px;
                font-family: Consolas;
                font-size: 11px;
                font-weight: 600;
            }

            #shortcutAction {
                font-size: 13px;
                color: palette(text);
            }


            /* =====================================
            Bottom
            ===================================== */

            #bottomFrame {
                border-top: 1px solid palette(midlight);
            }

            #closeButton {
                border: 1px solid palette(mid);
                border-radius: 7px;
                font-size: 13px;
                font-weight: 600;
            }
        """)

    # Create Card
    def createCard(self, title, text):
        card = self.createCardWidget()
        layout = card.layout()
        sectionTitle = self.createSectionTitle(title)
        layout.addWidget(sectionTitle)

        label = QtWidgets.QLabel(text)
        label.setObjectName("cardText")
        label.setWordWrap(True)

        label.setTextFormat(QtCore.Qt.TextFormat.RichText)
        layout.addWidget(label)
        return card

    # Create Card Widget
    def createCardWidget(self):
        card = QtWidgets.QFrame()
        card.setObjectName("card")

        layout = QtWidgets.QVBoxLayout(card)

        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        return card

    # Section Title
    def createSectionTitle(self, text):
        label = QtWidgets.QLabel(text)
        label.setObjectName("sectionTitle")
        return label

    # Calculation Row
    def createCalculationRow( self, name, expression, result):
        row = QtWidgets.QFrame()
        row.setObjectName("calculationRow")

        layout = QtWidgets.QHBoxLayout(row)

        layout.setContentsMargins(12, 8, 12, 8)

        nameLabel = QtWidgets.QLabel(name)
        nameLabel.setObjectName("calculationName")
        nameLabel.setFixedWidth(110)

        expressionLabel = QtWidgets.QLabel(expression)
        expressionLabel.setObjectName("calculationExpression")

        resultLabel = QtWidgets.QLabel(f"→ {result}")
        resultLabel.setObjectName("calculationResult")

        layout.addWidget(nameLabel)
        layout.addWidget(expressionLabel)
        layout.addStretch()
        layout.addWidget(resultLabel)

        return row

    # Shortcut Row
    def createShortcutRow(self,shortcut,action):
        row = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)

        key = QtWidgets.QLabel(shortcut)
        key.setObjectName("shortcutKey")
        key.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        key.setFixedHeight(28)
        key.setMinimumWidth(100)

        actionLabel = QtWidgets.QLabel(action)
        actionLabel.setObjectName("shortcutAction")

        layout.addWidget(key)
        layout.addSpacing(12)
        layout.addWidget(actionLabel)
        layout.addStretch()

        return row


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = HelpWindow()
    window.show()
    app.exec()