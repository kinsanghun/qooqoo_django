from django import template
from trade.models import *

register = template.Library()

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
    if p1 == p2: return "완납"
    elif p1 > 0: return "부분납부"
    else: return "미납"

