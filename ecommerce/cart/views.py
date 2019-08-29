from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart
from order.models import Order
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
    print(request.POST)
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
      else:      
            order_obj,new_order = Order.objects.get_or_create(cart=cart_obj)
      return render(request,"carts/checkout.html",{"object":order_obj})
