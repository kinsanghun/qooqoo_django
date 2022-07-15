from django.shortcuts import render, redirect
from main.editdate import *
from datetime import datetime
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

def parttimer(request):
    if request.method == "POST":
        return redirect("employee:parttimer")

    context = {
    }
    return render(request, "employee/parttimer.html", context)

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
        #employee work table에 값 넣기

        return
    name = request.GET.get("name", "None")
    d = request.GET.get("month", 0)
    if d:
        year = d.split("-")[0]
        month = d.split("-")[1]
    else:
        year = datetime.now().year
        month = datetime.now().month

    dates = getCalender(year, month)
    #employe model 불러오기
    employees = ""
    print(dates)
    #employee work table 불러오기
    context = {
        'name': name,
        'year': year,
        'month': month,
        'dates': dates,
        'employees': employees,
    }
    return render(request, "employee/workemployee.html", context)

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