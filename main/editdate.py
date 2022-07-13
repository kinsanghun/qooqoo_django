import calendar

def getCalender(year, month):
    result = list()
    c = calendar.Calendar()
    for date in c.itermonthdates(int(year), int(month)):result.append(date)
    return result