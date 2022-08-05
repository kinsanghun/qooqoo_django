from django.urls import path
from . import views

app_name = "trade"

urlpatterns = [
    path('client/', views.client, name="client"),
    path('client/getclient', views.getClient, name="getClient"),
    path('client/trade', views.clientTrade, name="clientTrade"),
    path('client/trade/get', views.getClientTrade, name="getClientTrade"),
    path('client/trade/edit', views.editTrade, name="editTrade"),
    path('client/trade/gettrade', views.getTrade, name="getTrade"),

    path('fix/', views.fix, name="fix"),
    path('fix/getFix', views.getFix, name="getFix"),
    path('fix/cost', views.fixCost, name="fixCost"),
    path('fix/cost/getCost', views.getFixCost, name="getFixCost"),

    path('manage/', views.manage, name="manage"),
    path('manage/getmanage', views.getManage, name="getmanage"),

    path('royalty/', views.royalty, name="royalty"),
    path('royalty/getRoyalty', views.getRoyalty, name="getRoyalty"),

    path('rant/', views.rant, name="rant"),
    path('rant/getrant', views.getRant, name="getRant"),
    path('rant/pay', views.rantPay, name="rantPay"),
    path('rant/pay/getRantPay', views.getRantPay, name="getRantPay"),

    path('etc/', views.etc, name="etc"),
    path('client/getetc', views.getEtc, name="getEtc"),

    path('etc/pay', views.etcPay, name="etcPay"),
    path('etc/pay/getPay', views.getEtcPay, name="getEtcPay"),

    path('cardinfo', views.cardinfo, name="cardinfo"),
    path('cardinfo/getinfo', views.getCardInfo, name="getcardinfo"),

    path('card', views.cardcost, name='cardcost'),
    path('card/getCost', views.getCardCost, name='getcardcost'),
]
