from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from ecommerce.utils import unique_slug_generator
from products.models import Product
class ProductTag(models.Model):
    title=models.CharField(max_length=120)
    slug=models.SlugField(blank=True,unique=True)
    timestamp=models.DateField(auto_now_add=True)
    active=models.BooleanField(default=True)
    products=models.ManyToManyField(Product,blank=True)
    def __str__(self):
        return self.title

def tag_presave(sender,instance,**args):
    if not instance.slug:
        instance.slug= unique_slug_generator(instance)
pre_save.connect(tag_presave,sender=ProductTag)        
