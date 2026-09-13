import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QDateTimeEdit
from PySide6.QtCore import QDateTime
#from countryinfo import CountryInfo
from datetime import date
from dateutil.relativedelta import relativedelta


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

start = date(2020, 6, 5)
end = date(2026, 9, 13)

result = end - start

total_days = result.days
weeks = total_days // 7
days = total_days % 7

difference = relativedelta(end, start)

print(f"Days: {total_days}")
print(f"Weeks: {weeks} weeks, {days} days")
print(f"Months: {difference.months} months, {difference.days} days")
print(f"Years: {difference.years} years, {difference.months} months, {difference.days} days")
