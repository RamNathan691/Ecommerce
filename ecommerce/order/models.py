from django.db import models
from cart.models import Cart
from ecommerce.utils import unique_order_idgenerator
from django.db.models.signals import pre_save,post_save
import math
from address.models import Address
from billing.models import Billingprofile
# Create your models here.
ORDER_STATUS_CHOICES=(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shippped'),
    ('refunded','Refunded'), 
)
class OrderManager(models.Manager):
    def new_or_get(self,billing_profile,cart_obj):
         order_qs=self.get_queryset().filter(billing_profile=billing_profile,cart=cart_obj,active=True) 
         created=False
         if order_qs.count()==1:
                  
                  order_obj=order_qs.first()
         else:
                 
                 order_obj=self.model.objects.create(billing_profile=billing_profile,cart=cart_obj)
                 created=True
         return order_obj,created
class Order(models.Model):
    billing_profile=  models.ForeignKey(Billingprofile,null=True,blank=True,on_delete=models.CASCADE)
    order_id       =  models.CharField(max_length=120,blank=True)
    cart           =  models.ForeignKey(Cart,on_delete=models.CASCADE)
    active         =  models.BooleanField(default=True)
    shipping_address= models.ForeignKey(Address,null=True,blank=True,related_name="shipping_address",on_delete=models.CASCADE)
    billing_address=  models.ForeignKey(Address,null=True,related_name="billing_adress",blank=True,on_delete=models.CASCADE)
    status         = models.CharField(max_length=120, default='created',choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=5.90,max_digits=10,decimal_places=2)
    total          = models.DecimalField(default=0.0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.order_id
    objects =OrderManager()
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


#this is baasically used for updating the cart total after the shipping address have been selected
def postsave_carttotal(sender,instance,created,*args,**kwargs):
    if not created:#if the cart is not ye created
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id
        qs=Order.objects.filter(cart__id=cart_id)#orange cart refers to the cart(model in the)
        if  qs.count()==1:
            order_obj=qs.first()#we get the current cart 
            order_obj.update_total()
post_save.connect(postsave_carttotal,sender=Cart)
#and this is for the Order total to get it updated
def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order )
