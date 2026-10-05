from PySide6 import QtWidgets, QtCore, QtGui
import qtawesome as qta
from Source.config import Settings

settings = Settings()

class SettingPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        Mainlayout = QtWidgets.QVBoxLayout(self)
        Mainlayout.setContentsMargins(10, 10, 10, 10)

        # The Title
        Lbl = QtWidgets.QLabel("Preferences")
        font = QtGui.QFont("Arial", 14)
        font.setBold(True)
        Lbl.setFont(font)

        #Rounding Contents Card
        roundingInput = QtWidgets.QSpinBox()
        roundingInput.setRange(0, 9)
        roundingInput.setValue(settings.RoundingValue)

        roundingContent = self.Additional_Widget("Provide rounding options", roundingInput)
        roundingCard = self.Create_Card("Rounding numbers", roundingContent)

        #Digit grouping seperator
        digCheck = QtWidgets.QCheckBox("Enable")
        digCheck.setChecked(settings.DigitGroup)

        digGroCard = self.Create_Card("Digit-Grouping Separator", digCheck)

        #Appearance
        appCombo = QtWidgets.QComboBox()
        appCombo.addItems(["Light", "Dark", "Auto"])
        appCombo.setCurrentText(settings.AppTheme)

        AppLayout = self.Additional_Widget("Change the app theme", appCombo)
        AppCard = self.Create_Card("Appearance", AppLayout)

        Mainlayout.addWidget(Lbl)
        Mainlayout.addWidget(roundingCard)
        Mainlayout.addWidget(digGroCard)
        Mainlayout.addWidget(AppCard)
        Mainlayout.addStretch()


    def Create_Card(self, title, *items):
        base = QtWidgets.QFrame()
        base.setObjectName("card")
        base.setStyleSheet("""
            QFrame#card {
                border: 1px solid gray;
                border-radius: 12px;
            }""")

        layout = QtWidgets.QVBoxLayout(base)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Card title
        Lbl = QtWidgets.QLabel(title)
        font = QtGui.QFont("Arial", 12)
        Lbl.setFont(font)
        layout.addWidget(Lbl)

        # Add widgets OR layouts
        for item in items:
            if isinstance(item, QtWidgets.QLayout):
                layout.addLayout(item)
            elif isinstance(item, QtWidgets.QWidget):
                layout.addWidget(item)

        return base

    def Additional_Widget(self, txt, widget):
        layoutBase = QtWidgets.QHBoxLayout()
        layoutBase.setObjectName("baseLayout")

        text = QtWidgets.QLabel(txt)
        font = QtGui.QFont("Arial", 10)
        text.setFont(font)
        text.setStyleSheet("color: gray;")

        layoutBase.addWidget(text)
        layoutBase.addStretch()
        layoutBase.addWidget(widget)

        return layoutBase