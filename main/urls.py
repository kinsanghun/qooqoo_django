from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index, name="index"),
    path('sales/', views.sales, name="sales"),
    path('misu_download', views.misu_download, name="misu_download"),
    path('delete', views.delete_func, name="delete"),
    path('tmp/', views.tmp, name="tmp"),
]
