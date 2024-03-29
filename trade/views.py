from django.shortcuts import render, redirect
from .models import *
from django.core import serializers
from django.http import HttpResponse
from main.utils import *
from main.editdate import *
import datetime


def client(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Client.objects.filter(id=data[0])

        if is_empty:
            model = Client.objects.get(id=data[0])
        else:
            model = Client()

        model.client = data[1]
        model.regnum = data[2]
        model.event = data[3]
        model.bank = data[4]
        model.banknum = data[5]
        model.callnum = data[6]
        model.is_card = data[7]
        model.status = data[8]
        model.save()

        return redirect("trade:client")
    datas = Client.objects.all()
    context = {
        'datas' : datas,
    }
    return render(request, "trade/client.html", context)

def getClient(request):
    key = request.GET.get("key")
    data = Client.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def clientTrade(request):
    if request.method == "POST":
        client = request.POST.get("client")
        date = request.POST.getlist("date[]")
        price = request.POST.getlist("price[]")
        content = request.POST.getlist("content[]")

        for i in range(len(date)):
            if price[i] == "" or price[i] == "0":
                continue
            trade = ClientTrade.objects.filter(client=client, date=date[i], price__gt=0)

            if(len(trade)):
                model = ClientTrade.objects.get(client=client, date=date[i], price__gt=0)

                model.content = content[i]
                model.price = price[i]

            else:
                model = ClientTrade()

                model.client = client
                model.date = date[i]
                model.price = price[i]
                model.pay = 0
                model.content = content[i]

            model.save()

        return redirect("trade:clientTrade")


    date = datetime.datetime.now().strftime("%Y-%m-%d")

    filter_client = request.GET.get("client", "all")
    filter_start = request.GET.get("start", "1000-01") + "-01"
    filter_end = request.GET.get("end", "9999-12")

    filter_end += f"-{str(getLastDatOfTheMonth(int(filter_end.split('-')[0]), int(filter_end.split('-')[1])))}"

    if filter_client == "all":
        trading = ClientTrade.objects.filter(date__range=[filter_start, filter_end]).order_by("-date")
        misu_chk = ClientTrade.objects.all()
    else:
        trading = ClientTrade.objects.filter(client=filter_client, date__range=[filter_start, filter_end]).order_by("-date")
        misu_chk = ClientTrade.objects.filter(client=filter_client).all()

    total = 0
    select_total = 0
    for trade in trading:
        select_total += trade.price

    for trade in misu_chk:
        total += trade.price - trade.pay

    client = Client.objects.values("client")

    context = {
        'today': datetime.datetime.strptime(date, "%Y-%m-%d"),
        'clients': client,
        'datas': trading,
        'select_total': select_total,
        'misu': total,
        'filter_client': filter_client,
    }
    if filter_start.split("-")[0] != "1000":
        context["filter_start"] = datetime.datetime.strptime(filter_start, "%Y-%m-%d")
        context["filter_end"] = datetime.datetime.strptime(filter_end, "%Y-%m-%d")

    print(date, context["today"])

    return render(request, "trade/client_trade.html", context)

def editTrade(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = ClientTrade.objects.filter(id=data[0])

        if len(model) == 0:
            model = ClientTrade()
        else:
            model = ClientTrade.objects.get(id=data[0])

        model.date = data[1]
        model.client = data[2]
        model.price = data[3]
        model.pay = data[4]
        model.content = data[5]
        model.card = data[6]
        model.save()

    return redirect("trade:clientTrade")

def getClientTrade(request):
    key = request.GET.get("key")
    data = ClientTrade.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def getTrade(request):
    client = request.GET.get("client")
    month = request.GET.get("month")
    input = month.split("-")
    start = f"{input[0]}-{input[1]}-01"
    end = f"{input[0]}-{input[1]}-{getLastDatOfTheMonth(int(input[0]), int(input[1]))}"
    data = ClientTrade.objects.filter(client=client, date__range=[start, end], price__gt=0)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def fix(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Fix.objects.filter(id=data[0])

        if is_empty:
            model = Fix.objects.get(id=data[0])
        else:
            model = Fix()

        model.fix = data[1]
        model.event = data[2]
        model.paytype = data[3]
        model.save()

        return redirect("trade:fix")

    datas = Fix.objects.all()

    context = {
        'datas' : datas,
    }
    return render(request, "trade/fixcost.html", context)

def getFix(request):
    key = request.GET.get("key")
    data = Fix.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def fixCost(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = FixCost.objects.filter(id=data[0])
        target = Fix.objects.get(fix=data[2])

        if is_empty:
            model = FixCost.objects.get(id=data[0])
        else:
            model = FixCost()

        model.date = data[1] + "-01"
        model.fix = data[2]

        if target.paytype == "자동이체":
            model.price = data[3]
            model.pay = data[3]
        else:
            print(data[4])
            if data[4] == "1":
                model.price = data[3]
                model.pay = data[3]
            else:
                model.price = data[3]
                model.pay = 0

        model.content = data[5]
        model.save()

        return redirect("trade:fixCost")

    fix = Fix.objects.all()
    datas = FixCost.objects.all()
    context = {
        'fix': fix,
        'datas': datas,
    }
    return render(request, "trade/fixTrade.html", context)


def getFixCost(request):
    key = request.GET.get("key")
    data = FixCost.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def royalty(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Royalty.objects.filter(id=data[0])

        if is_empty:
            model = Royalty.objects.get(id=data[0])
        else:
            model = Royalty()

        model.date = data[1] + "-01"
        model.royalty = data[2]
        model.price = data[3]
        model.pay = data[4]
        model.content = data[5]
        model.save()

        return redirect("trade:royalty")

    start = request.GET.get("start", "-1")

    if start != "-1":
        datas = Royalty.objects.filter(date__year=start).all()
    else:
        datas = Royalty.objects.all()

    context = {
        'datas': datas,
        "start": start,
    }
    return render(request, "trade/royalty.html", context)

def getRoyalty(request):
    key = request.GET.get("key")
    data = Royalty.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


def rant(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Rant.objects.filter(id=data[0])

        if is_empty:
            model = Rant.objects.get(id=data[0])
        else:
            model = Rant()

        model.rant = data[1]
        model.landload = data[2]
        model.bank = data[3]
        model.banknum = data[4]
        model.pay = data[5]
        model.surtax = data[6]
        model.content = data[7]
        model.save()

        return redirect("trade:rant")

    datas = Rant.objects.all()
    context = {
        'datas' : datas,
    }
    return render(request, "trade/rant.html", context)


def getRant(request):
    key = request.GET.get("key")
    data = Rant.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def rantPay(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = RantPay.objects.filter(id=data[0])

        if is_empty:
            model = RantPay.objects.get(id=data[0])
        else:
            model = RantPay()

        model.date = data[1]
        model.rant = data[2]
        model.price = data[3]
        model.pay = data[4]
        model.content = data[5]
        model.save()

        return redirect("trade:rantPay")

    rants = Rant.objects.all()
    datas = RantPay.objects.all()

    context = {
        'rants': rants,
        'datas': datas,
    }
    return render(request, "trade/rantPay.html", context)

def getRantPay(request):
    key = request.GET.get("key")
    data = RantPay.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def etc(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Etc.objects.filter(id=data[0])

        if is_empty:
            model = Etc.objects.get(id=data[0])
        else:
            model = Etc()

        model.etc = data[1]
        model.pay = data[2]
        model.paytype = data[3]
        model.summary = data[4]
        model.content = "-"
        model.save()

        return redirect("trade:etc")

    datas = Etc.objects.all()
    context = {
        'datas' : datas,
    }
    return render(request, "trade/etc.html", context)

def getEtc(request):
    key = request.GET.get("key")
    data = Etc.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def etcPay(request):
    if request.method == "POST":
        id = request.POST.get("id")
        date = request.POST.get("date")
        etc = request.POST.get("etc")
        summary = request.POST.get("summary")
        row = Etc.objects.get(etc=etc)
        pay = request.POST.get("pay")

        if id != "-1":
            model = EtcPay.objects.get(id=id)
        else:
            model = EtcPay()

        model.date = date
        model.summary = summary
        model.etc = row.etc
        model.price = row.pay
        model.paytype = row.paytype

        if row.paytype == "자동이체" or row.paytype == "카드결제":
            model.pay = row.pay
        else:
            if pay == "":
                pay = 0
            model.pay = pay

        model.content = ""

        model.save()

        return redirect("trade:etcPay")

    etc = Etc.objects.all()
    datas = EtcPay.objects.all()

    context = {
        'etcs': etc,
        'datas': datas,
    }
    return render(request, "trade/etcPay.html", context)

def getEtcPay(request):
    key = request.GET.get("key")
    data = EtcPay.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def manage(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Manage.objects.filter(id=data[0])

        if is_empty:
            model = Manage.objects.get(id=data[0])
        else:
            model = Manage()

        model.date = data[1] + "-01"
        model.price = data[2]
        model.status = data[3]
        model.content = data[4]
        model.save()

        return redirect("trade:manage")

    datas = Manage.objects.all()

    context = {
        'datas': datas,
    }
    return render(request, "trade/manage.html", context)

def getManage(request):
    key = request.GET.get("key")
    data = Manage.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def cardinfo(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = CardInfo.objects.filter(id=data[0])

        if is_empty:
            model = CardInfo.objects.get(id=data[0])
        else:
            model = CardInfo()

        model.card = data[1]
        model.content = data[2]
        model.save()

        return redirect("trade:cardinfo")

    datas = CardInfo.objects.all()

    context = {
        'datas': datas,
    }
    return render(request, "trade/cardinfo.html", context)

def getCardInfo(request):
    key = request.GET.get("key")
    data = CardInfo.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def cardcost(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = CardCost.objects.filter(id=data[0])

        if is_empty:
            model = CardCost.objects.get(id=data[0])
        else:
            model = CardCost()

        model.date = data[1] + "-01"
        model.card = data[2]
        model.cost = data[3]
        model.content = data[4]
        model.save()
        return redirect("trade:cardcost")

    datas = CardCost.objects.all()
    context = {
        'datas': datas,
    }
    return render(request, "trade/cardcost.html", context)


def getCardCost(request):
    key = request.GET.get("key")
    data = CardCost.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")