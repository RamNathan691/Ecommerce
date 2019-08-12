from django.db import models

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=50)
    descrpition=models.TextField(max_length=1000)
    price=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    image=models.ImageField(upload_to="products/",null=True,blank=True)
    def __str__(self):
        return self.title


class ProductManager(models.Manager):
    def get_by_id (self,id):
        qs=self.get_queryset().filter(id=id)
        if qs.count () ==1:
            return qs.first ()    
        return None