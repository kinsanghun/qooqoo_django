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
        print(len(is_empty))

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
            trade = ClientTrade.objects.filter(client=client, date=date[i])

            if(len(trade)):
                model = ClientTrade.objects.get(client=client, date=date[i])
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
    else:
        trading = ClientTrade.objects.filter(client=filter_client, date__range=[filter_start, filter_end]).order_by("-date")


    client = Client.objects.values("client")

    context = {
        'today':date,
        'clients':client,
        'datas':trading,
        'filter_client':filter_client,
        'filter_start':filter_start,
        'filter_end':filter_end,
    }
    return render(request, "trade/client_trade.html", context)

def editTrade(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = ClientTrade.objects.get(id=data[0])

        model.date = data[1]
        model.client = data[2]
        model.price = data[3]
        model.pay = data[4]
        model.content = data[5]
        model.save()

    return redirect("trade:clientTrade")

def getClientTrade(request):
    key = request.GET.get("key")
    data = ClientTrade.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def getTrade(request):
    client = request.GET.get("client")
    start = request.GET.get("start")
    end = request.GET.get("end")

    data = ClientTrade.objects.filter(client=client, date__range=[start, end])
    post_list = serializers.serialize('json', data)
    print(data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def clientTradeBatch(request):
    if request.method == "GET":
        client = request.GET.get("client")
        start = request.GET.get("start")
        end = request.GET.get("end")
        print(client, start, end)

        if client == "all":
            datas = ClientTrade.objects.filter(date__range=[start, end])
        else :
            datas = ClientTrade.objects.filter(client=client, date__range=[start, end])

        for data in datas:
            data.pay = data.price
            data.save()

    return redirect("trade:clientTrade")

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
    return render(request, "trade/royalty.html")

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

        model.date = data[1]
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

def manage(request):
    return render(request, "trade/manage.html")