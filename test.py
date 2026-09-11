import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateTimeEdit
from PySide6.QtCore import QDateTime
#from countryinfo import CountryInfo


#app = QApplication(sys.argv)

#window = QWidget()
#layout = QVBoxLayout(window)

#datetime_picker = QDateTimeEdit()
#datetime_picker.setDateTime(QDateTime.currentDateTime())
#datetime_picker.setCalendarPopup(True)
#datetime_picker.setDisplayFormat("dd/MM/yyyy")

#layout.addWidget(datetime_picker)

#window.show()
#sys.exit(app.exec())




#def convert(value, from_unit, to_unit):
#    return (value * ureg(from_unit)).to(to_unit)

from countryinfo import all_countries

countries = all_countries()

for country in countries:
    currencies = country.currencies()

    if currencies:
        print(f"{country.name()}: {currencies[0]}")
