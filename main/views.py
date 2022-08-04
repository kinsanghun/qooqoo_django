from django.shortcuts import render, redirect
from .reporting import tradeReport, SQL
from datetime import datetime, timedelta
from .crawling import *
from .models import *
from trade.models import *

def a_few_months_ago(year, month, n):
    return f"{str(year - 1)}-{str(month + 12 - n).rjust(2, '0')}-01" if month - n <= 0 else f"{str(year)}-{str(month - n).rjust(2, '0')}-01"


def profit_or_loss():
    sql = SQL()

    dist = list()
    labor = list()
    card = list()
    profit = list()

    two_month_ago = a_few_months_ago(datetime.now().year, datetime.now().month, 2)


    query = f"select strftime('%Y-%m', month) as month, sum(price) as price from main_sales where month >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            profit.append({'month': datetime.strptime(r[0]+"-01", "%Y-%m-%d"), 'price': r[1]})
        while len(profit) < 3:
            profit.insert(0, {'month': datetime.now(), 'price': 0})

    query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_clientTrade where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            dist.append({'month': datetime.strptime(r[0]+"-01", "%Y-%m-%d"), 'price': r[1]})
        while len(dist) < 3:
            dist.insert(0, {'month': datetime.now(), 'price': 0})

    query = f"select strftime('%Y-%m', date) as month, sum(cost) as price from employee_laborCost where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            labor.append({'month': datetime.strptime(r[0] + "-01", "%Y-%m-%d"), 'price': r[1]})
        while len(labor) < 3:
            labor.insert(0, {'month': datetime.now(), 'price': 0})

    query = f"select strftime('%Y-%m', date) as month, sum(cost) as price from trade_cardCost where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            card.append({'month': datetime.strptime(r[0] + "-01", "%Y-%m-%d"), 'price': r[1]})
        while len(card) < 3:
            card.insert(0, {'month': datetime.now(), 'price': 0})

    # profit or loss
    result = [0, 0, 0]
    if len(profit) >= 3:
        for i in range(0, 3):
            result[i] = profit[i]["price"] - dist[i]["price"] - labor[i]["price"] - card[i]["price"]

    return result

def month3(year, month):
    return [f"{str(year-1)}년 {str(month+12-2)}월" if month-2 <= 0 else f"{str(year)}년 {str(month-2)}월",
            f"{str(year-1)}년 {str(month+12-1)}월" if month-1 <= 0 else f"{str(year)}년 {str(month-1)}월",
            f"{str(year)}년 {str(month)}월"]


def index(request):
    two_month_ago = a_few_months_ago(datetime.now().year, datetime.now().month, 2)

    selected = request.GET.get("selected", "매출")
    sql = SQL()
    datas = list()
    if selected == "매출":
        query = f"select strftime('%Y-%m', month) as group_month, sum(price) as price from main_sales where month >= '{two_month_ago}' group by group_month order by group_month desc limit 3";

    elif selected == "물류":
        query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_clientTrade where date >= '{two_month_ago}' group by month order by month desc limit 3";

    elif selected == "인건비":
        query = f"select strftime('%Y-%m', date) as month, sum(cost) as price from employee_laborCost where date >= '{two_month_ago}'group by month order by month desc limit 3";

    elif selected == "법인카드":
        query = f"select strftime('%Y-%m', date) as month, sum(cost) as price from trade_cardCost where date >= '{two_month_ago}' group by month order by month desc limit 3";

    res = sql.select(query)

    if res:
        for r in res:
            datas.append({'month': datetime.strptime(r[0]+"-01", "%Y-%m-%d"), 'price': r[1]})
        while len(datas) < 3:
            datas.insert(0, {'month': datetime.now(), 'price': 0})

    profitorloss = profit_or_loss()
    report = tradeReport()

    client_misu = report.client_misu()
    fix_misu = report.fix_misu()
    royal_misu = report.royal_misu()
    manage_misu = report.manage_misu()
    rant_misu =report.rant_misu()

    print(profitorloss)
    context = {
        #graph
        'profitorloss': profitorloss,
        'selected': selected,
        'datas':datas,

        #misu
        'misu_clients': client_misu,
        'misu_fixs': fix_misu,
        'misu_royals': royal_misu,
        'misu_manages': manage_misu,
        'misu_rants': rant_misu,
    }
    return render(request, "main/index.html", context)

def insert_sales(sales):
    for sale in sales:
        try:
            model = Sales.objects.filter(month=sale[0] + "-01")
            if len(model):
                model = Sales.objects.get(month=sale[0] + "-01")
                if model.price == sale[1]:
                    continue
            else:
                model = Sales()

            model.month = sale[0] + "-01"
            model.price = sale[1]
            model.save()
        except:
            pass

def sales(request):
    if request.method == "POST":

        id = request.POST.get("id")
        pw = request.POST.get("pw")

        data = web_crawling(id, pw)
        insert_sales(data)

        return redirect("main:sales")


    datas = Sales.objects.all()

    context = {
        'datas': datas,
    }
    return render(request, "main/sales.html", context)

def tmp(request):
    return render(request, "main/tmp..html")