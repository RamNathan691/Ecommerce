from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart
from order.models import Order
from account.models import GuestEmail
from account.forms import LoginForm,GuestForm
from billing.models import Billingprofile
from address.forms import AddressForm
# Create your views here.
def cart_home(request):
    #del request.session['cart_id']
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    products=cart_obj.products.all()
    return render(request,"carts/home.html",{"cart":cart_obj}) 

    #print(key)
    #request.session.set_expiry(300)
     #so whenever you go to the the page that you are passing this data when you go to that page you can find the users name
    #how to create a session variable
      #if cart_id is None:  #and isinstance(cart_id,int):
       #cart_obj=Cart.objects.create(user=None)
     #   request.session['cart_id']=cart_obj.id
    #else:
def cart_update(request):
    
    product_id=request.POST.get('product_id')
    if product_id is not None:
      product_obj=Product.objects.get(id=product_id)
      print(product_obj)
      cart_obj,new_obj=Cart.objects.new_or_get(request)
      if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
      else:
            cart_obj.products.add(product_obj)
      request.session['cart_items']= cart_obj.products.count()
    return redirect('carthome')
def checkout_home(request):
      cart_obj,new_obj=Cart.objects.new_or_get(request)
      order_obj=None
      if new_obj or cart_obj.products.count() == 0:
            return redirect('carthome')
      user=request.user
      login_form=LoginForm()
      guest_form=GuestForm()
      address_form=AddressForm()
      billing_address_form=AddressForm()
      billing_profile=None
      guest_email_id=request.session.get('guest_email')
      if user.is_authenticated:
               billing_profile,billing_profile_created=Billingprofile.objects.get_or_create(user=user,email=user.email)
      elif  guest_email_id is not None:
            guest_obj=GuestEmail.objects.get(id=guest_email_id)
            billing_profile,billing_guest_profile_created=Billingprofile.objects.get_or_create(email=guest_obj.email)
      else: 
            pass
      if billing_profile is not None:
            order_qs=Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True) 
            if order_qs.count()==1:
                  order_obj=order_qs.first()
            else:
                  order_obj=Order.objects.create(billing_profile=billing_profile,cart=cart_obj)
                 
      context={
                  "object":order_obj,
                  "billingprofile":billing_profile,
                  "login":login_form,
                  "guest_form":guest_form,
                  "billing_address_form":billing_address_form,
                  "address_form":address_form
            }
      return render(request,"carts/checkout.html",context)
 
