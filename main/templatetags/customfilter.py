import datetime

from django import template
from trade.models import *
from employee.models import *

register = template.Library()


# calendar
@register.filter
def is_true(a, b):
    if int(a) == int(b):
        return 1
    else:
        return 0


@register.filter
def is_false(a, b):
    if int(a) != int(b):
        return 1
    else:
        return 0


@register.filter
def is_card(data):
    if data:
        return "카드결제"
    else:
        return ""


@register.filter
def hello(client):
    trades = ClientTrade.objects.filter(client=client)
    totalpay = 0
    totalprice = 0

    for trade in trades:
        totalpay += trade.pay
        totalprice += trade.price

    return totalprice - totalpay


@register.filter
def output_pay(p1, p2):
    if p1 == 0:
        return p2
    else:
        return p1


@register.filter
def output_type(p1):
    if p1 != 0:
        return "매입"
    else:
        return "입금"


@register.filter
def misu_client(client):
    datas = ClientTrade.objects.filter(client=client)
    a = 0
    b = 0
    for data in datas:
        a += data.price
        b += data.pay

    if a == b:
        return "N"
    return "Y"


@register.filter
def royalty_status(p1, p2):
    if p1 == p2:
        return "완납"
    elif p1 > 0:
        return "부분납부"
    else:
        return "미납"


@register.filter
def convert_pay(pay):
    if pay < 0:
        return str((int((pay * -1) % 100_000_000) * -1) // 10000)
    else:
        return str(int(pay % 100_000_000) // 10000)


@register.filter
def is_uk(pay):
    uk = ""
    if pay < 0:
        pay *= -1
    if pay // 100_000_000:
        uk = str(pay // 100_000_000)
    return uk


@register.filter
def print_pay(pay):
    if pay < 0:
        pay *= -1
        if pay >= 100_000_000:
            return f" - {is_uk(pay)}억 {str(int(pay % 100_000_000) // 10000)}"
        else:
            return f" - {str(int(pay % 100_000_000) // 10000)}"
    else:
        if pay >= 100_000_000:
            return f"{is_uk(pay)}억 {str(int(pay % 100_000_000) // 10000)}"
        else:
            return f"{str(int(pay % 100_000_000) // 10000)}"


@register.filter
def isWork(date, employee):
    try:
        target = WorkStaff.objects.get(date=date, name=employee)
        return True
    except:
        return False


@register.filter
def getWork(date, employee):
    return WorkStaff.objects.get(date=date, name=employee)

@register.filter
def getWorkColor(worktype):
    color = {
        "출근": "#FFBA00",
        "조퇴": "#38C7D9ee",
        "연차": "#EB6772cc",
        "반차": "#EB6772cc",
        "주휴일": "#4174A0bb",
        "반주휴": "#4174A0bb",
        "결근": "#50505099",
        "추가근로": "#5AB769"
    }
    return color[worktype]

@register.filter
def convertMinuteToTime(m):
    return f"{m // 60}:{str(m % 60).rjust(2, '0')}"

@register.filter
def isBefore(now, month):
    if now == "today":
        today = datetime.date.today()
        inwork = month
        if (today - inwork).days >= 365:
            return False
        return True

    now_year = int(now.split("-")[0])
    now_month = int(now.split("-")[1])
    target_year = int(month.split("-")[0])
    target_month = int(month.split("-")[1])

    if now_year >= target_year:
        if now_month > target_month:
            return True
        else:
            return False
    else:
        return False
