from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=30)
    reg_num = models.CharField(max_length=30)
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    bank = models.CharField(max_length=20)
    bank_num = models.CharField(max_length=30)
    inwork = models.DateField()
    department = models.CharField(max_length=30)
    rank = models.CharField(max_length=30)
    worksystem = models.IntegerField()
    pay = models.IntegerField()
    insurance = models.CharField(max_length=20)
    health = models.CharField(max_length=30)
    content = models.TextField()