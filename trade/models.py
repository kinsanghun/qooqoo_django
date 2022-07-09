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
    card = models.IntegerField(default=0)
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
    summary = models.CharField(max_length=50)
    etc = models.CharField(max_length=40)
    pay = models.IntegerField()
    paytype = models.CharField(max_length=20)
    content = models.TextField()

class EtcPay(models.Model):
    date = models.DateField()
    summary = models.CharField(max_length=50)
    etc = models.CharField(max_length=40)
    price = models.IntegerField()
    pay = models.IntegerField()
    paytype = models.CharField(max_length=20)
    content = models.TextField()


class Royalty(models.Model):
    date = models.DateField()
    royalty = models.CharField(max_length=50)
    price = models.IntegerField()
    pay = models.IntegerField()
    content = models.TextField()

class Manage(models.Model):
    date = models.DateField()
    price = models.IntegerField()
    status = models.CharField(max_length=20)
    content = models.TextField()
