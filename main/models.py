from django.db import models

class Sales(models.Model):
    month = models.DateField()
    price = models.IntegerField()

class Banks(models.Model):
    bank = models.CharField(max_length=30)
