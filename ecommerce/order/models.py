from django.db import models
from cart.models import Cart
from ecommerce.utils import unique_order_idgenerator
from django.db.models.signals import pre_save,post_save
# Create your models here.
ORDER_STATUC_CHOICES=(
    ('created','Created'),
    ('paid','Paid'),
    ('shipped','Shippped'),
    ('refunded','Refunded'), 
)
class Order(models.Model):
    order_id=models.CharField(max_length=120,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    
    status=models.CharField(max_length=120,default='created',choices=ORDER_STATUC_CHOICES)
    #shipping_total
    shipping_total=models.DecimalField(default=59.0,max_digits=10,decimal_places=2)
    total=models.DecimalField(default=0.0,max_digits=10,decimal_places=2)

    def __str__(self):
        return self.order_id
    def update_total(self):
        cart_total=self.cart_total
        shipping_total=self.shipping_total
        new_total=cart_total + shipping_total
        self.total=new_total
        self.save()
        return new_total
def presave_create_order_id(sender,instance,*args,**kwargs):
    if not instance.order_id:
        instance.order_id=unique_order_idgenerator(instance)

pre_save.connect(presave_create_order_id,sender=Order)

def postsave_carttotal(sender,instance,created,*args,**kwargs):
    if not created:
        cart_obj=instance
        cart_total=cart_obj.total
        cart_id=cart_obj.id
        qs=Order.objects.filter(cart_id=cart_id)
        if qs.exists() and qs.count()==1:
            order_obj=qs.first()
            order_obj.update_total()
post_save.connect(postsave_carttotal,sender=Order)

def post_save_order(sender,instance,created,*args,**kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order,sender=Order )
