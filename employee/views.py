from django.shortcuts import render, redirect
from main.editdate import *
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from main.utils import *
from .models import *
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
        return redirect("employee:oneday")

    context = {
    }
    return render(request, "employee/oneday.html", context)

def manageAnnual(request):
    context = {

    }
    return render(request, "employee/manageAnnual.html", context)

def retired(request):
    context = {

    }
    return render(request, "employee/retired.html", context)

def workemployee(request):
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

        return redirect("employee:workEmployee")

    employees = Employee.objects.all()
    name = request.GET.get("name", employees[0].name)
    d = request.GET.get("month", False)

    if d:
        year = d.split("-")[0]
        month = d.split("-")[1]
    else:
        year = datetime.now().year
        month = datetime.now().month

    dates = getCalender(year, month)
    #employee work table 불러오기
    work = WorkEmployee.objects.filter(date__year=year, date__month=month).all()
    print(work)
    context = {
        'works': work,
        'name': name,
        'year': year,
        'month': str(month).rjust(2, "0"),
        'dates': dates,
        'employees': employees,
    }
    return render(request, "employee/workemployee.html", context)

def getWorkEmployee(request):
    name = request.GET.get("name")
    date = request.GET.get("date")
    data = WorkEmployee.objects.filter(name=name, date=date)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def workparttimer(request):
    return

def workonday(request):
    return

def managePay(request):
    return

def schedule(request):
    return

def turnover(request):
    return