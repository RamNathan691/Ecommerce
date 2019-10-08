from django.db import models
from cart.models import Cart
from ecommerce.utils import unique_order_idgenerator
from django.db.models.signals import pre_save,post_save
import math
from billing.models import Billingprofile
# Create your models here.
ORDER_STATUC_CHOICES=(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shippped'),
    ('refunded','Refunded'), 
)


class Order(models.Model):
    billing_profile=models.ForeignKey(Billingprofile,null=True,blank=True,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=120,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    active=models.BooleanField(default=True)
    
    status=models.CharField(max_length=120,default='created',choices=ORDER_STATUC_CHOICES)
   
    shipping_total=models.DecimalField(default=5.90,max_digits=10,decimal_places=2)
    total=models.DecimalField(default=0.0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.order_id
    def update_total(self):
        cart_total=self.cart.total
        shipping_total=self.shipping_total
        new_total=math.fsum([cart_total , shipping_total])
        formatted_total=format(new_total,'.2f')
        self.total=formatted_total
        self.save()
        return formatted_total
   
def presave_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_idgenerator(instance)
    qs=Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists:
        qs.update(active=False)
pre_save.connect(presave_create_order_id,sender=Order)

def postsave_carttotal(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id
        qs=Order.objects.filter(cart__id=cart_id)
        if  qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()
post_save.connect(postsave_carttotal,sender=Cart)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order )
