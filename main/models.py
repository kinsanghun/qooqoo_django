from django.db import models

class Sales(models.Model):
    month = models.DateField()
    price = models.IntegerField()

# Create your models here.
