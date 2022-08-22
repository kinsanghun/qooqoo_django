import calendar


def getCalendar(year, month):
    result = list()
    c = calendar.Calendar(firstweekday=6)
    for date in c.itermonthdates(int(year), int(month)):result.append(date)
    return result

def getLastDatOfTheMonth(year, month):
    lastdays = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    year = int(year)
    month = int(month)

    if month == 2:
        if year % 400 == 0:
            return lastdays[month] + 1
        elif year % 100 == 0:
            return lastdays[month]
        elif year % 4 == 0:
            return lastdays[month] + 1

    else:
        return lastdays[month]

def convertTimeToMinute(time, isFloat=False):
    if not isFloat:
        year, month = map(int, time.split(":"))
        return (year * 60) + month
    else:
        if "." in time:
            return (int(float(time)) * 60) + 30
        else:
            return int(time) * 60