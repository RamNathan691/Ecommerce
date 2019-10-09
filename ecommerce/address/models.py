from django.db import models
from billing.models import Billingprofile

ADDRESS_TYPES=(
    ('billing','billing'),
    ('shipping','shipping')
)
class Address(models.Model):
    billing_profile = models.ForeignKey(Billingprofile,on_delete=models.CASCADE)
    addressType = models.CharField(max_length=120,choices=ADDRESS_TYPES)
    addressline1 = models.CharField(max_length=120)
    addressline2 = models.CharField(max_length=120,null=True,blank=True)
    city    =        models.CharField(max_length=120)
    state    =       models.CharField(max_length=120)
    country  =   models.CharField(max_length=120,default="India")
    postalcode  =    models.CharField(max_length=120)
    

    def __str__(self):
        return self.addressType