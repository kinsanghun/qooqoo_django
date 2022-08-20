from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from main.editdate import *
from main.utils import *
from .annual import *

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

        if data[2].split("-")[1][0] == "1" or data[2].split("-")[1][0] == "3":model.gender = "남"
        else:model.gender = "여"

        model.bank = data[5]
        model.bank_num = data[6]
        model.inwork = data[7]

        if data[8]:
            model.outwork = data[8]
        model.department = data[9]
        model.rank = data[10]
        model.worksystem = data[11]
        model.pay = data[12]
        model.insurance = data[13]
        model.health = data[14]
        model.content = data[15]
        model.notreport = data[16]

        model.save()

        return redirect("employee:employee")

    datas = Employee.objects.filter(outwork__isnull=True).all()
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

        if data[2].split("-")[1][0] == "1" or data[2].split("-")[1][0] == "3":model.gender = "남"
        else:model.gender = "여"

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
        model.notreport = data[14]

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
        annuals.append({
            "name": l.get_name(),
            "annual": l.get_annual(),
            "used": len(WorkEmployee.objects.filter(name=l.get_name(), annual=1))
        })

    context = {
        'annuals':annuals,
    }
    return render(request, "employee/manageAnnual.html", context)

def retired(request):
    target = request.GET.get("target", "employee")

    if target == "employee":
        datas = Employee.objects.filter(outwork__isnull=False).all()
    else:
        datas = Parttimer.objects.filter(outwork__isnull=False).all()

    context = {
        'target': target,
        'datas': datas,
    }
    return render(request, "employee/retired.html", context)

def workemployee(request):
    if request.method == "POST":

        datas = list()

        inputName = ["workDate",
                      "workName",
                      "workType",
                      "workStart",
                      "workEnd",
                      "breakTime",
                      "workContent"]

        for name in inputName:
            datas.append(request.POST.get(name))

        if WorkStaff.objects.filter(date=datas[0], name=datas[1]):
            model = WorkStaff.objects.get(date=datas[0], name=datas[1])
        else:
            model = WorkStaff()

        model.date = datas[0]
        model.name = datas[1]
        model.worktype = datas[2]
        model.workstart = convertTimeToMinute(datas[3])
        model.workend = convertTimeToMinute(datas[4])

        if datas[5]:
            model.breaktime = convertTimeToMinute(time=datas[5], isFloat=True)
        else:
            model.breaktime = 0

        if datas[6]:
            model.content = datas[6]
        else:
            model.content = ""

        model.save()

        return redirect("employee:workEmployee")

    error = ""

    # Create Employee Data
    employees = Employee.objects.all()

    # If Don't have Employee data
    if not employees:
        return render(request, "employee/employee.html", {'error': "직원을 먼저 생성해주세요."})

    # Get Request
    requestGetEmployee = request.GET.get("employee", employees[0].name)
    requestGetDate = request.GET.get("date", datetime.now().strftime("%Y-%m"))

    year = requestGetDate.split("-")[0]
    month = requestGetDate.split("-")[1]

    # Create Calendar
    calendar = getCalendar(year, month)
    workDatas = WorkStaff.objects.filter(name=requestGetEmployee, date__year=year, date__month=month)

    # Context
    context = {
        'employees': employees,
        'calendar': calendar,
        'workdatas': workDatas,

        'selectedEmployee': requestGetEmployee,
        'year': year,
        'month': month,

        'error': error,
    }
    return render(request, "employee/workemployee.html", context)

def getWorkEmployee(request):
    name = request.GET.get("name")
    date = request.GET.get("date")
    data = WorkEmployee.objects.filter(name=name, date=date)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")

def del_workemployee(request):
    name = request.GET.get("name")
    date = request.GET.get("date")
    try:
        target = WorkEmployee.objects.get(name=name, date=date)
        target.delete()

    finally:
        return redirect("employee:workEmployee")

def workparttimer(request):

    if request.method == "POST":

        # Base Data
        name = request.POST.get("name")
        month = list(map(int, request.POST.get("month").split("-")))

        # Input Data
        dates = request.POST.getlist("dates[]")
        times = request.POST.getlist("times[]")
        contents = request.POST.getlist("contents[]")

        # target Month Data Clear
        WorkParttimer.objects.filter(name=name, date__year=month[0], date__month=month[1]).delete()

        # Input Work Data
        for i in range(len(dates)):
            if times[i]:
                model = WorkParttimer()
                model.name = name
                model.date = dates[i]
                model.time = times[i]
                model.content = contents[i]
                model.save()

        return redirect("employee:workParttimer")

    # Get Parttimer List

    dates = list()
    name = ""
    parttimers = Parttimer.objects.all()

    if parttimers:
        name = request.GET.get("parttimer", parttimers[0].name)

    # Month Setting
    date = request.GET.get("month", datetime.now().strftime("%Y-%m"))
    year, month = date.split("-")

    for date in getCalendar(year, month):
        if int(month) == date.month:
            dates.append({'date':date, 'time':'', 'content':''})

    # Get Parttimer work
    works = WorkParttimer.objects.filter(name=name, date__year=year, date__month=month)

    # Mapping Work and Date
    for work in works:
        for i in range(len(dates)):
            if work.date.strftime("%Y-%m-%d") == dates[i]['date'].strftime("%Y-%m-%d"):
                dates[i]['time'] = work.time if work.time else ''
                dates[i]['content'] = work.content
                break

    # Context
    context = {
        'works': works,
        'name': name,
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
            target = Oneday.objects.get(id=data[2])
            model.name = target.name
            model.reg_num = target.reg_num
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

#인건비 
def laborCost(request):
    if request.method == "POST":
        data = getPOSTValue(request.POST)
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