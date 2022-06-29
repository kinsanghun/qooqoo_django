from django.db import models

# Create your models here.

class Client(models.Model):
    client = models.CharField(max_length=40)
    regnum = models.CharField(max_length=20)
    event = models.CharField(max_length=20)
    bank = models.CharField(max_length=20)
    banknum = models.CharField(max_length=20)
    callnum = models.CharField(max_length=20)
    status = models.CharField(max_length=10)

class ClientTrade(models.Model):
    date = models.DateField()
    client = models.CharField(max_length=40)
    price = models.IntegerField()
    pay = models.IntegerField()
    content = models.TextField()

class Fix(models.Model):
    fix = models.CharField(max_length=50)
    event = models.CharField(max_length=30)
    paytype = models.CharField(max_length=15)

class FixCost(models.Model):
    date = models.DateField()
    fix = models.CharField(max_length=50)
    price = models.IntegerField()
    pay = models.IntegerField()
    content = models.TextField()

class Rant(models.Model):
    rant = models.CharField(max_length=40)
    landload = models.CharField(max_length=20)
    bank = models.CharField(max_length=20)
    banknum = models.CharField(max_length=20)
    pay = models.CharField(max_length=20)
    surtax = models.CharField(max_length=20)
    content = models.TextField()

class RantPay(models.Model):
    date = models.DateField()
    rant = models.CharField(max_length=50)
    price = models.IntegerField()
    pay = models.IntegerField()
    content = models.TextField()

class Etc(models.Model):
    date = models.DateField()
    etc = models.CharField(max_length=40)
    pay = models.CharField(max_length=20)
    paytype = models.CharField(max_length=20)
    content = models.TextField()

