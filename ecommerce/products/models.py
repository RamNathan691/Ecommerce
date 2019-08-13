from django.db import models

# Create your models here.
class ProductManager(models.Manager):
    def get_by_id(self,id):
        qs=self.get_queryset().filter(id=id)
        if qs.count () == 1:
            return qs.first ()    
        return None


class Product(models.Model):
    title=models.CharField(max_length=50)
    slug =models.SlugField(blank=True)
    descripition=models.TextField(max_length=1000)
    price=models.DecimalField(max_digits=10, decimal_places=2,default=0.0)
    image=models.ImageField(upload_to="products/",null=True,blank=True)
    featured=models.BooleanField(default=False)
    active=models.BooleanField(default=True)
    def __str__(self):
        return self.title
    objects=ProductManager()    

