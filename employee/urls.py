from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path('employee', views.employee, name="employee"),
    path('employee/getemployee', views.getemployee, name="getEmployee"),

    path('parttimer', views.parttimer, name="parttimer"),
    path('parttimer/getparttimer', views.getparttimer, name="getParttimer"),

    path('oneday', views.oneday, name="oneday"),
    path('oneday/getOneday', views.getOneday, name="getOneday"),

    path('workemployee', views.workemployee, name="workEmployee"),
    path('workemployee/getWork', views.getWorkEmployee, name="getWorkEmployee"),

    path('workparttimer', views.workparttimer, name="workParttimer"),

    path('workoneday', views.workoneday, name="workoneday"),
    path('workoneday/getWork', views.getWorkOneday, name="getworkoneday"),

    path('manageAnnual', views.manageAnnual, name="manageAnnual"),
]
