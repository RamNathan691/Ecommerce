from django.db import models

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=50)
    descrpition=models.CharField(max_length=1000)
    price=models.DecimalField(max_digits=5, decimal_places=2,default=0.0)

