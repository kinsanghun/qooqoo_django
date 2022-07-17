import calendar


def getCalendar(year, month):
    result = list()
    c = calendar.Calendar(firstweekday=6)
    for date in c.itermonthdates(int(year), int(month)):result.append(date)
    return result
