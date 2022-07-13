from django.shortcuts import render, redirect
from main.editdate import *
from datetime import datetime
# Create your views here.


def employee(request):
    if request.method == "POST":
        return redirect("employee:employee")

    context = {
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