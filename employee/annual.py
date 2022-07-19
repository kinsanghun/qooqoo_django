from .models import *
from datetime import datetime

def convertStringToDate(year, month, day):
    return datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

class Annual:
    def __init__(self, id):
        self.employee = Employee.objects.get(id=id)

    def get_name(self):
        return self.employee.name

    def get_inwork(self):
        return self.employee.inwork

    def get_inwork_year(self):
        return self.employee.inwork.year

    def get_inwork_month(self):
        return self.employee.inwork.month

    def get_inwork_day(self):
        return self.employee.inwork.day

    def is_after_a_year(self, date):
        inwork = datetime.strptime(f"{date.year+1}-{date.month}-{date.day}","%Y-%m-%d")
        now = datetime.now()
        if now >= inwork:
            return True
        else:
            return False

    def get_annual(self):
        annual = 0
        year_annual = 0
        count = 0
        year = self.get_inwork_year()
        month = self.get_inwork_month()
        day = self.get_inwork_day()

        now_year = datetime.now().year
        now_month = datetime.now().month

        while convertStringToDate(year, month, 1) <= datetime.now() and annual < 12:
            if count == 0:
                if month >= 12:
                    year += 1
                    month = 1
                else:
                    month += 1
                count += 1
                continue

            if len(WorkEmployee.objects.filter(date__year=year, date__month=month, working="결근")) == 0:
                annual += 1

            print(year, month)
            if month >= 12:
                year += 1
                month = 1
            else:
                month += 1

        if self.is_after_a_year(self.get_inwork()):
            date = self.get_inwork()
            i = 1
            while True:
                inwork = datetime.strptime(f"{date.year + i}-{date.month}-{date.day}", "%Y-%m-%d")
                if inwork <= datetime.now():
                    i+=1
                    year_annual += 15
                else:
                    break

        return annual + year_annual