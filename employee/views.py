from django.shortcuts import render, redirect

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
