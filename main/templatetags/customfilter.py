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
def misu_client(client):
    datas = ClientTrade.objects.filter(client=client)
    for data in datas:
        print(data.price, data.pay)
        if data.price - data.pay > 0:
            return "Y"
    return "N"
