from django.shortcuts import render, redirect
from .reporting import tradeReport, SQL
from datetime import datetime
from .crawling import *
from .models import *
from trade.models import *


def month3(year, month):
    return [f"{str(year-1)}년 {str(month+12-2)}월" if month-2 <= 0 else f"{str(year)}년 {str(month-2)}월",
            f"{str(year-1)}년 {str(month+12-1)}월" if month-1 <= 0 else f"{str(year)}년 {str(month-1)}월",
            f"{str(year)}년 {str(month)}월"]

def index(request):
    selected = request.GET.get("selected", "매출")
    sql = SQL()
    if selected == "매출":
        datas = Sales.objects.all().order_by("-month")[:3]
        print(datas)
    elif selected == "물류":
        query = "select strftime('%Y-%m', date) as month, sum(price) as price from trade_clientTrade group by month limit 3";
        res = sql.select(query)
        datas = list()
        if res:
            for r in reversed(res):
                datas.append({'month':datetime.strptime(r[0]+"-01", "%Y-%m-%d"), 'price':r[1]})
    elif selected == "인건비":
        datas = list()
    elif selected == "법인카드":
        datas = list()
        
    conn = tradeReport()
    client_misu = conn.client_misu()
    fix_misu = conn.fix_misu()
    rant_misu = conn.rant_misu()

    context = {
        #graph
        'selected': selected,
        'datas':datas,

        #misu
        'client_misus': client_misu,
        'fix_misus': fix_misu,
        'rant_misus': rant_misu,
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