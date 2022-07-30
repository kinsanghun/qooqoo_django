from django.shortcuts import render, redirect
from main.editdate import *
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from main.utils import *
from .models import *
from .annual import *

import os
import pandas, openpyxl
# Create your views here.

def employee(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = Employee.objects.filter(id=data[0])

        if len(model) == 0:
            model = Employee()
        else:
            model = Employee.objects.get(id=data[0])

        model.name = data[1]
        model.reg_num = data[2]
        model.contact = data[3]
        model.gender =  data[4]
        model.bank =  data[5]
        model.bank_num = data[6]
        model.inwork = data[7]
        model.department = data[8]
        model.rank = data[9]
        model.worksystem = data[10]
        model.pay = data[11]
        model.insurance = data[12]
        model.health = data[13]
        model.content = data[14]

        model.save()

        return redirect("employee:employee")
    datas = Employee.objects.all()
    context = {
        'datas': datas,
    }
    return render(request, "employee/employee.html", context)

def getemployee(request):
    key = request.GET.get("key")
    data = Employee.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


def parttimer(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = Parttimer.objects.filter(id=data[0])

        if len(model) == 0:
            model = Parttimer()
        else:
            model = Parttimer.objects.get(id=data[0])

        model.name = data[1]
        model.reg_num = data[2]
        model.contact = data[3]
        model.gender = data[4]
        model.pay = data[5]
        model.bank = data[6]
        model.bank_num = data[7]
        model.department = data[8]
        model.part = data[9]
        model.inwork = data[10]
        if data[11]:
            model.outwork = data[11]
        model.health = data[12]
        model.content = data[13]

        model.save()

        return redirect("employee:parttimer")
    datas = Parttimer.objects.all()
    context = {
        'datas': datas,
    }
    return render(request, "employee/parttimer.html", context)

def getparttimer(request):
    key = request.GET.get("key")
    data = Parttimer.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def oneday(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = Oneday.objects.filter(id=data[0])

        if len(model) == 0:
            model = Oneday()
        else:
            model = Oneday.objects.get(id=data[0])

        model.name = data[1]
        model.reg_name = data[2]
        model.contact = data[3]
        model.save()

        return redirect("employee:oneday")

    datas = Oneday.objects.all()
    context = {
        'datas': datas,
    }
    return render(request, "employee/oneday.html", context)


def getOneday(request):
    key = request.GET.get("key")
    data = Oneday.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def manageAnnual(request):
    employee_list = list()
    employees = Employee.objects.all()
    for employee in employees:
        employee_list.append(Annual(employee.id))

    annuals = []

    for l in employee_list:
        annuals.append({"name":l.get_name(), "annual":l.get_annual(),
                        "used":len(WorkEmployee.objects.filter(name=l.get_name(), annual=1))})

    print(annuals)
    context = {
        'annuals':annuals,
    }
    return render(request, "employee/manageAnnual.html", context)

def retired(request):
    context = {

    }
    return render(request, "employee/retired.html", context)

def workemployee(request):
    url = "employee/workemployee.html"
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = WorkEmployee.objects.filter(name=data[1], date=data[2])

        if len(model) == 0:
            model = WorkEmployee()
        else:
            model = WorkEmployee.objects.get(name=data[1], date=data[2])

        model.name = data[1]
        model.date = data[2]
        model.working = data[3]
        model.start = data[4]
        model.end = data[5]
        if len(data[7]) > 0:
            model.extra_type = data[6]
            model.extra = data[7]

        model.dayoff = data[8]
        model.annual = data[9]
        model.content = data[10]

        model.save()

    employees = Employee.objects.all()
    name = request.GET.get("name", employees[0].name)
    d = request.GET.get("month", False)

    if d:
        year = d.split("-")[0]
        month = d.split("-")[1]
    else:
        year = datetime.now().year
        month = datetime.now().month

    dates = getCalendar(year, month)
    #employee work table 불러오기
    work = WorkEmployee.objects.filter(date__year=year, date__month=month).all()

    context = {
        'request':request.method,
        'works': work,
        'name': name,
        'year': year,
        'month': str(month).rjust(2, "0"),
        'dates': dates,
        'employees': employees,
    }
    return render(request, url, context)

def getWorkEmployee(request):
    name = request.GET.get("name")
    date = request.GET.get("date")
    data = WorkEmployee.objects.filter(name=name, date=date)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def workparttimer(request):
    if request.method == "POST":
        name = request.POST.get("name")

        dates = request.POST.getlist("dates[]")
        times = request.POST.getlist("times[]")
        contents = request.POST.getlist("contents[]")

        for i, date in enumerate(dates):
            if times[i]:
                works = WorkParttimer.objects.filter(name=name, date=date)
                if works:
                    model = WorkParttimer.objects.get(name=name, date=date)
                else:
                    model = WorkParttimer()

                model.name = name
                model.date = date
                model.time = times[i]
                model.content = contents[i]

                model.save()

                print(name, i, date, times[i])

        return redirect("employee:workParttimer")

    parttimers = Parttimer.objects.all()
    if len(parttimers):
        name = request.GET.get("name", parttimers[0].name)
    else:
        name = ""
    year = request.GET.get("year", datetime.now().year)
    month = request.GET.get("month", datetime.now().month)
    dates = list()
    for date in getCalendar(year, month):
        if month == date.month:dates.append(date)

    works = WorkParttimer.objects.filter(name=name, date__month=month)
    context = {
        'works':works,
        'name':name,
        'dates': dates,
        'year': year,
        'month': str(month).rjust(2, "0"),
        'parttimers': parttimers,
    }
    return render(request, "employee/workparttimer.html", context)

def workoneday(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        model = WorkOneday.objects.filter(id=data[0])

        if len(model) == 0:
            model = WorkOneday()
            target = Oneday.objects.get(id=data [2])
            model.name = target.name
            model.reg_num = target.reg_name
        else:
            model = WorkOneday.objects.get(id=data[0])

        model.date = data[1]
        model.pay = data[3]
        model.content = data[4]

        model.save()

        return redirect("employee:workoneday")

    oneday = Oneday.objects.all()
    datas = WorkOneday.objects.all()
    context = {
        'onedays':oneday,
        'datas':datas,
    }
    return render(request, "employee/workOneday.html",context)


def getWorkOneday(request):
    key = request.GET.get("key")
    data = WorkOneday.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def managePay(request):
    return

def schedule(request):
    return

def turnover(request):
    return


#인건비 
def laborCost(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
        print(data[0])
        model = LaborCost.objects.filter(id=data[0])

        if len(model) == 0:
            model = LaborCost()
        else:
            model = LaborCost.objects.get(id=data[0])

        model.date = data[1] + "-01"
        model.department = data[2]
        model.rank = data[3]
        model.cost = data[4]
        model.save()

        return redirect('employee:laborCost')

    employees = Employee.objects.filter(outwork__isnull=True)
    datas = LaborCost.objects.all()

    context = {
        'employees':employees,
        'datas' : datas,
    }
    return render(request, "employee/laborcost.html", context)

def getLaborCost(request):
    key = request.GET.get("key")
    data = LaborCost.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")