from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth import authenticate
from django.db.models.signals import pre_save,m2m_changed
User = settings.AUTH_USER_MODEL
# Create your models here.
class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id=request.session.get("cart_id",None)
        q=self.get_queryset().filter(id=cart_id)
        if q.count()==1:
            new_obj=False
            cart_obj=q.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user=request.user
                cart_obj.save()
        else: 
             cart_obj=Cart.objects.new_cart(user=request.user)
             new_obj=True
             request.session['cart_id']=cart_obj.id
        return cart_obj,new_obj     

    def new_cart(self,user=None):# Basically this functio is used to create the CART object for us and this is similar to the CREATE function
        user_obj=None
        if user is not None:
            if user.is_authenticated:
                user_obj=user
        return self.model.objects.create(user=user_obj)
class Cart(models.Model): 
    user =models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,blank=True)
    total=models.DecimalField(default=0.0,max_digits=10,decimal_places=2)
    updated=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
     
    objects=CartManager()   

def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
    if action =='post_add' or action=='post_remove' or action=='post_clear':
        products=instance.products.all()
        total =0
        for x in products:
            total += x.price
        instance.total=total
        instance.save()

m2m_changed.connect(m2m_changed_cart_receiver,sender=Cart.products.through)

