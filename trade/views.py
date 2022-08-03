from django.shortcuts import render, redirect
from .models import *
from django.core import serializers
from django.http import HttpResponse
from main.utils import *
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
        model.status = data[7]
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
        print(date, price, content)

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
            print(trade)

        return redirect("trade:clientTrade")


    date = datetime.datetime.now().strftime("%Y-%m-%d")
    s = date.split("-")
    s[2] = "01"
    filter_client = request.GET.get("client", "all")
    filter_start = request.GET.get("start", "-".join(s))
    filter_end = request.GET.get("end", date)

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
        'today': date,
        'clients': client,
        'datas': trading,
        'select_total': select_total,
        'misu': total,
        'filter_client': filter_client,
        'filter_start': filter_start,
        'filter_end': filter_end,
    }
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
    if data[0].pay == 0 and data[0].price != 0:return HttpResponse("")

    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def getTrade(request):
    client = request.GET.get("client")
    start = request.GET.get("start")
    end = request.GET.get("end")

    data = ClientTrade.objects.filter(client=client, date__range=[start, end], price__gt=0)
    post_list = serializers.serialize('json', data)
    print(data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def fix(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Fix.objects.filter(id=data[0])
        print(len(is_empty))

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
        print(len(is_empty))

        if is_empty:
            model = FixCost.objects.get(id=data[0])
        else:
            model = FixCost()

        model.date = data[1]
        model.fix = data[2]
        model.price = data[3]
        model.pay = data[4]
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
    end = request.GET.get("end", "-1")

    if start != "-1" or end != "-1":
        datas = Royalty.objects.filter(date__range=[start + "-01", end + "-02"]).all()
    else:
        datas = Royalty.objects.all()

    context = {
        'datas': datas,
        "start": start,
        "end": end,
    }
    return render(request, "trade/royalty.html", context)

def getRoyalty(request):
    key = request.GET.get("key")
    data = Royalty.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    print(post_list)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


def rant(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        is_empty = Rant.objects.filter(id=data[0])
        print(len(is_empty))

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
        print(len(is_empty))

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
        print(len(is_empty))

        if is_empty:
            model = Etc.objects.get(id=data[0])
        else:
            model = Etc()

        model.summary = data[1]
        model.etc = data[2]
        model.pay = data[3]
        model.paytype = data[4]
        model.content = data[5]
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
        summary = request.POST.get("summary")
        content = request.POST.get("content")
        row = Etc.objects.get(summary=summary)

        if id != "-1":
            model = EtcPay.objects.get(id=id)
        else:
            model = EtcPay()

        model.date = date
        model.summary = summary
        model.etc = row.etc
        model.price = row.pay
        model.paytype = row.paytype

        if row.paytype == "자동이체":
            model.pay = row.pay
        else:
            model.pay = 0
        model.content = content

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