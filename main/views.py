from django.shortcuts import render, redirect
from django.http import HttpResponse
from .reporting import tradeReport, SQL
from datetime import datetime, timedelta
from django.db import connection
from .crawling import *
from .models import *

import pandas as pd


try:
    from io import BytesIO as IO  # for modern python
except ImportError:
    from io import StringIO as IO  # for legacy python

from trade.models import *
def get_exceldownload(df):
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    df.to_excel(xlwriter, 'sheetname')
    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename ="foo.xlsx"'
    return response

def a_few_months_ago(year, month, n):
    return f"{str(year - 1)}-{str(month + 12 - n).rjust(2, '0')}-01" if month - n <= 0 else f"{str(year)}-{str(month - n).rjust(2, '0')}-01"


def profit_or_loss():
    sql = SQL()
    m_2 = a_few_months_ago(datetime.now().year, datetime.now().month, 2)
    m_1 = a_few_months_ago(datetime.now().year, datetime.now().month, 1)
    m_0 = a_few_months_ago(datetime.now().year, datetime.now().month, 0)
    dist = {m_2: 0, m_1: 0, m_0: 0}
    labor = {m_2: 0, m_1: 0, m_0: 0}
    card = {m_2: 0, m_1: 0, m_0: 0}
    fix = {m_2: 0, m_1: 0, m_0: 0}
    royalty = {m_2: 0, m_1: 0, m_0: 0}
    profit = {m_2: 0, m_1: 0, m_0: 0}
    rant = {m_2: 0, m_1: 0, m_0: 0}
    manage = {m_2: 0, m_1: 0, m_0: 0}
    etc = {m_2: 0, m_1: 0, m_0: 0}

    two_month_ago = a_few_months_ago(datetime.now().year, datetime.now().month, 2)

    #매출
    query = f"select strftime('%Y-%m', month) as month, sum(price) as price from main_sales where month >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            profit[r[0]+"-01"] = r[1]

    #물류
    query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_clientTrade where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            dist[r[0]+"-01"] = r[1]

    #인건비
    query = f"select strftime('%Y-%m', date) as month, sum(cost) as price from employee_laborCost where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            labor[r[0]+"-01"] = r[1]

    #고정비
    query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_fixCost where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            fix[r[0]+"-01"] = r[1]

    #로열티
    query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_royalty where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            royalty[r[0]+"-01"] = r[1]

    #기타
    query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_etcPay where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            etc[r[0]+"-01"] = r[1]

    #관리비
    query = f"select strftime('%Y-%m', date) as month, sum(price) from trade_manage where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            manage[r[0]+"-01"] = r[1]

    #임대료
    query = f"select strftime('%Y-%m', date) as month, sum(price) as price from trade_rantpay where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            rant[r[0]+"-01"] = r[1]

    #카드대금
    query = f"select strftime('%Y-%m', date) as month, sum(cost) as price from trade_cardCost where date >= '{two_month_ago}' group by month order by month desc limit 3";
    res = sql.select(query)
    if res:
        for r in res:
            card[r[0]+"-01"] = r[1]

    # profit or loss
    result = [0, 0, 0]
    if len(profit) >= 3:
        for i, d in enumerate([m_0, m_1, m_2]):
            result[i] = profit[d] - dist[d] - labor[d] - card[d] - rant[d] - manage[d] - etc[d] - fix[d] - royalty[d]

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

def model_to_cecel(model):
    params = None

    if model == "client":
        sql = ("select"
               " client.client as '거래처',"
               " client.regnum as '사업자등록번호',"
               " client.event as '종목',"
               " client.bank as '은행',"
               " client.banknum as '계좌번호',"
               " client.callnum as '연락처',"
               " client.status as '계약상태',"
               " sum(trade.price-trade.pay) as '미수금'"
               " from trade_client client, trade_clientTrade trade"
               " where client.client = trade.client and"
               " trade.price - trade.pay > 0"
               " group by client.client")

    elif model == "fix":
        sql = ("select"
               " fix.fix as '고정비명',"
               " fix.event as '종목',"
               " fix.paytype as '납부타입',"
               " sum(cost.price-cost.pay) as '미수금'"
               " from trade_fix fix, trade_fixCost cost"
               " where fix.fix=cost.fix and"
               " cost.price - cost.pay > 0"
               " group by cost.fix")

    elif model == "royalty":
        sql = ("select"
               " date as '날짜',"
               " royalty as '로열티',"
               " (price - pay) as '미수금',"
               " content as '비고'"
               " from trade_royalty"
               " where (price - pay) > 0 order by date")

    elif model == "manage":
        sql = ("select"
               " strftime('%Y년 %m월', date) as '날짜',"
               " price as '미수금',"
               " content as '비고'"
               " from trade_manage"
               " where status='미납'")

    elif model == "rant":
        sql = ("select"
               " rant.rant as '호수',"
               " rant.landload as '임대인',"
               " rant.bank as '은행',"
               " rant.banknum as '계좌번호',"
               " sum(pay.price - pay.pay) as '미납임대료'"
               " from trade_rant rant, trade_rantpay pay"
               " where rant.rant=pay.rant and"
               " pay.price - pay.pay > 0"
               " group by pay.rant")

    df = pd.read_sql_query(sql, connection, params=params)
    return df

def misu_download(request):
    misu = request.GET.get("target", "-1")
    if misu == "-1":
        return redirect("main:index")

    df = model_to_cecel(misu)
    response = get_exceldownload(df)
    return response

def tmp(request):
    return render(request, "main/tmp..html")