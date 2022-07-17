from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path('employee', views.employee, name="employee"),
    path('employee/getemployee', views.getemployee, name="getEmployee"),

    path('parttimer', views.parttimer, name="parttimer"),
    path('parttimer/getparttimer', views.getparttimer, name="getParttimer"),

    path('oneday', views.oneday, name="oneday"),

    path('workemployee', views.workemployee, name="workEmployee"),
    path('workemployee/getWork', views.getWorkEmployee, name="getWorkEmployee"),

    path('workparttimer', views.workparttimer, name="workParttimer"),
]
