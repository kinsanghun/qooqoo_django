from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('sales/', views.sales, name="sales"),
    path('tmp/', views.tmp, name="tmp"),
]
