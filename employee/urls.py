from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    path('employee', views.employee, name="employee"),
    path('parttimer', views.parttimer, name="parttimer"),
    path('oneday', views.oneday, name="oneday"),
]
