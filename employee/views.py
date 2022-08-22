from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
from django.db import connection
from main.editdate import *
from main.utils import *
from .annual import *
import pandas as pd

try:
    from io import BytesIO as IO  # for modern python
except ImportError:
    from io import StringIO as IO  # for legacy python


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

        if data[2].split("-")[1][0] == "1" or data[2].split("-")[1][0] == "3":
            model.gender = "남"
        else:
            model.gender = "여"

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

        if data[2].split("-")[1][0] == "1" or data[2].split("-")[1][0] == "3":
            model.gender = "남"
        else:
            model.gender = "여"

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
        'annuals': annuals,
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
    data = WorkStaff.objects.filter(name=name, date=date)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


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
            dates.append({'date': date, 'time': '', 'content': ''})

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
        'onedays': oneday,
        'datas': datas,
    }
    return render(request, "employee/workOneday.html", context)


def getWorkOneday(request):
    key = request.GET.get("key")
    data = WorkOneday.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


# 인건비
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
        'employees': employees,
        'datas': datas,
    }
    return render(request, "employee/laborcost.html", context)


def getLaborCost(request):
    key = request.GET.get("key")
    data = LaborCost.objects.filter(id=key)
    post_list = serializers.serialize('json', data)
    return HttpResponse(post_list, content_type="text/json-comment-filtered")


def employeeIO(request):
    # Data Setting
    year, month = request.GET.get("date", datetime.today().strftime("%Y-%m")).split("-")

    inworkEmployee = Employee.objects.filter(inwork__year=year, inwork__month=month, outwork__isnull=True).all()
    outworkEmployee = Employee.objects.filter(outwork__year=year, outwork__month=month).all()
    context = {
        'inworks': inworkEmployee,
        'outworks': outworkEmployee,
    }
    return render(request, "employee/employeeIO.html", context)


def employeeReportSetting(target, year, month):
    _daysOfMonth = getLastDatOfTheMonth(year, month)

    result = {
        'name': target.name,
        'depoartment': target.department,
        'rank': target.rank,
        'reg_num': target.reg_num,
        'worksystem': target.worksystem,
        'inwork': target.inwork,
        'outwork': target.outwork,
        'pay': target.pay,
        'daysofmonth': _daysOfMonth,
        'dedays': 0,
        'detime': 0,
        'plustime': 0,
        'bank': target.bank,
        'bank_num': target.bank_num,
        'insurance': target.insurance,
        'content': ""
    }
    works = WorkStaff.objects.filter(name=result["name"], date__year=year, date__month=month)

    if result["worksystem"] == 5:
        aveWorkTime = 9 * 60 + 30
    else:
        aveWorkTime = 9 * 60

    for work in works:
        if work.worktype == "출근" or work.worktype == "조퇴":
            worktime = work.workend - work.workstart - work.breaktime
            if aveWorkTime > worktime:
                result["detime"] += (aveWorkTime - worktime) / 60

        if work.worktype == "추가근로":
            worktime = work.workend - work.workstart - work.breaktime
            result["plustime"] += (worktime / 60)

        if work.worktype == "결근":
            result["daysofmonth"] -= 1
            result["dedays"] += 1

    return result


def parttimerReportSetting(target, year, month):
    _daysOfMonth = getLastDatOfTheMonth(year, month)

    result = {
        'name': target.name,
        'depoartment': "파트",
        'pay': target.pay,
        'reg_num': target.reg_num,
        'inwork': target.inwork,
        'outwork': target.outwork,
        'total': 0,
        'bank': target.bank,
        'bank_num': target.bank_num,
        'content': ""
    }
    total = 0

    # Exploring this month's work
    for i in range(1, _daysOfMonth + 1):
        date = f"{year}-{str(month).rjust(2, '0')}-{str(i).rjust(2, '0')}"
        weekday = datetime.strptime(date, "%Y-%m-%d").weekday()

        # Initialize variables after aggregation every Monday
        if weekday == 0:
            if total >= 15:
                result["total"] += (total * result["pay"]) + (total * result["pay"] / 5)
            else:
                result["total"] += (total * result["pay"])

            total = 0

        # Get information for the day
        target = WorkParttimer.objects.filter(date=date, name=result["name"])
        if target:
            total += target[0].time

    # Last week's process
    if total >= 15:
        result["total"] += (total * result["pay"]) + (total * result["pay"] / 5)
    else:
        result["total"] += (total * result["pay"])

    result["total"] = int(result["total"])

    return result


def workReport(request):
    employee_datas = list()
    parttimer_datas = list()

    # get Data
    date = request.GET.get("month", datetime.today().strftime("%Y-%m")).split("-")
    year = date[0]
    month = date[1]
    employees = Employee.objects.all()

    # Setting Work Data
    for employee in employees:
        employee_datas.append(employeeReportSetting(employee, year=year, month=month))

    parttimers = Parttimer.objects.all()
    for parttimer in parttimers:
        parttimer_datas.append(parttimerReportSetting(parttimer, year=year, month=month))

    # Context
    context = {
        'year': year,
        'month': month,
        'report_employee': employee_datas,
        'report_parttimer': parttimer_datas,
    }
    return render(request, "employee/workReport.html", context)


def downloadWorkReport(request):
    employee_datas = list()
    parttimer_datas = list()

    year = request.GET.get("year")
    month = request.GET.get("month")
    employees = Employee.objects.all()
    parttimers = Parttimer.objects.all()

    # Setting Work Data
    employee_columns = ["이름", "부서", "직급", "주민등록번호", "근무제", "입사일"
        , "퇴사일", "계약임금", "월급여계산일수", "공제(일)", "공제(시간)",
                        "추가수당(시간)", "은행", "계좌번호", "사대보험 가입여부", "비고"]

    parttimer_columns = ["이름", "구분", "시급", "주민등록번호", "입사일", "퇴사일",
                         "지급액", "은행", "계좌번호", "비고"]

    # Create Data
    for employee in employees:
        employee_datas.append(employeeReportSetting(employee, year=year, month=month))

    for parttimer in parttimers:
        parttimer_datas.append(parttimerReportSetting(parttimer, year, month))

    # Convert Dict To DataFrame
    employee_df = pd.DataFrame(employee_datas)
    employee_df.columns = employee_columns

    parttimer_df = pd.DataFrame(parttimer_datas)
    parttimer_df.columns = parttimer_columns

    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    employee_df.to_excel(xlwriter, f'직원근태인계{month}월')
    parttimer_df.to_excel(xlwriter, f"파트타이머근태인계{month}월")

    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)

    # Export Setting
    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename ="work_report_{year}-{month}.xlsx"'
    return response


def IOdownload(request):
    # Data Setting
    params = None

    date = request.GET.get("date", datetime.today().strftime("%Y-%m"))
    year = date.split("-")[0]
    month = date.split("-")[1]

    inwork = ("select name as '이름',"
              " reg_num as '주민등록번호',"
              " department as '직급',"
              " rank as '파트',"
              " worksystem as '근무제',"
              " inwork as '입사일',"
              " outwork as '퇴사일',"
              " pay as '계약임금',"
              " content as '비고' from employee_Employee"
              " where outwork is null"
              " and strftime('%Y', inwork)='" + year + "'"
                                                       " and strftime('%m', inwork)='" + month + "'"
                                                                                                 " order by inwork DESC")

    outwork = ("select name as '이름',"
               " reg_num as '주민등록번호',"
               " department as '직급',"
               " rank as '파트',"
               " worksystem as '근무제',"
               " inwork as '입사일',"
               " outwork as '퇴사일',"
               " pay as '계약임금',"
               " content as '비고' from employee_Employee"
               " where strftime('%Y', outwork)='" + year + "'"
                                                           " and strftime('%m', outwork)='" + month + "'"
                                                                                                      " order by outwork DESC")

    inwork_df = pd.read_sql_query(inwork, connection, params=params)
    outwork_df = pd.read_sql_query(outwork, connection, params=params)

    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

    inwork_df.to_excel(xlwriter, '입사자현황')
    outwork_df.to_excel(xlwriter, '퇴사자현황')

    xlwriter.save()
    xlwriter.close()
    excel_file.seek(0)

    response = HttpResponse(excel_file.read(),
                            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename ="employee_status_{year}-{month}.xlsx"'
    return response
