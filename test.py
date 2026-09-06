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




def convert(value, from_unit, to_unit):
    return (value * ureg(from_unit)).to(to_unit)
