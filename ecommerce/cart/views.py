from django.http import JsonResponse
from django.shortcuts import render,redirect
from products.models import Product
from .models import Cart
from order.models import Order
from account.models import GuestEmail
from account.forms import LoginForm,GuestForm
from billing.models import Billingprofile
from address.forms import AddressForm
from address.models import Address
# Create your views here.
def cart_detail_api_view(request):
      cart_obj,new_obj=Cart.objects.new_or_get(request)
      products=[{"name":x.title,"price":x.price, "url":x.get_absolute_url(), "id":x.id} for x in cart_obj.products.all()]#[<object>,<object>,<object>]
      cartdata={"products":products,"total":cart_obj.total,}
      return JsonResponse(cartdata)
def cart_home(request):
    #del request.session['cart_id']
    cart_obj,new_obj=Cart.objects.new_or_get(request)
    products=cart_obj.products.all()
    return render(request,"carts/home.html",{"cart":cart_obj}) 
#THIS IS THE VERY IMPORTANT OF THIS PROJECT TO KNOW
    #print(key)
    #request.session.set_expiry(300)
    #so whenever you go to the the page that you are passing this data when you go to that page you can find the users name
    #how to create a session variable
    #if cart_id is None:  isinstance(cart_id,int):#the isinstance part is used to check whether the session value is string or integer and not any other datatype
    #cart_obj=Cart.objects.create(user=None)
    #request.session['cart_id']=cart_obj.id
    #else:
    #print("cart ID EXISTS")
def cart_update(request):
    
    product_id=request.POST.get('product_id')
    if product_id is not None:
      product_obj=Product.objects.get(id=product_id)
      cart_obj,new_obj=Cart.objects.new_or_get(request)
      if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added=False
      else:
            cart_obj.products.add(product_obj)
            added=True
      request.session['cart_items']= cart_obj.products.count()
    if request.is_ajax():
          print("ajax")
          json_data={
                "added":added,
                "removed":not added,
                "cartItemCount":cart_obj.products.count(),
          }
          return JsonResponse(json_data)
    return redirect('carthome')
def checkout_home(request):
      cart_obj,new_obj=Cart.objects.new_or_get(request)#we are getting the current session cart
      order_obj=None                                   #get_or_create is build in function
      if new_obj or cart_obj.products.count() == 0:
            return redirect('carthome')#if the cart is just now created in the above line then go to carthome(Cart is empty)
      user=request.user
      login_form=LoginForm()
      guest_form=GuestForm()
      address_form=AddressForm()
      billing_address_id=request.session.get("billing_address_id",None)
      shipping_address_id=request.session.get("shipping_address_id",None)
      billing_profile=None
      guest_email_id=request.session.get('guest_email')
      if user.is_authenticated:
               billing_profile, billing_profile_created=Billingprofile.objects.get_or_create(user=user,email=user.email)
      elif  guest_email_id is not None:
            guest_obj=GuestEmail.objects.get(id=guest_email_id)
            billing_profile,billing_guest_profile_created=Billingprofile.objects.get_or_create(email=guest_obj.email)
      else: 
            pass
      address_qs=None
      #so basically the billingprofile is created for the user above but if he logs back again then we shouldnt keep on create an order we should retrieve it and produce it
      if billing_profile is not None:
            if request.user.is_authenticated:
            #order_qs=Order.objects.filter(billing_profile=billing_profile,cart=cart_obj,active=True) 
            #if order_qs.count()==1:this entire thing moved to the oredermanager
             #     order_obj=order_qs.first()
            #else:
                  address_qs =Address.objects.filter(billing_profile=billing_profile)
            order_obj,order_obj_created=Order.objects.new_or_get(billing_profile,cart_obj)
            if shipping_address_id:
                         order_obj.shipping_address=Address.objects.get(id=shipping_address_id)
                         order_obj.save()
                         del request.session["shipping_address_id"]
            if billing_address_id:
                             order_obj.billing_address=Address.objects.get(id=billing_address_id)
                             order_obj.save()
                             del request.session["billing_address_id"]

       #we are gonna update the oder as we are completed the checkout process
       #so we deletet the cart_id
       #and redirect it to the success
       #these 3 we are gonna perform
      if request.method =="POST":
            #checking for that order to be done
            #del request.session['cart_id']
            done=order_obj.check_done()
            if done:
                  order_obj.mark_paid()
                  del request.session['cart_id']
                  request.session['cart_items']=0;
                  return redirect("success")



              
      context={
                  "object":order_obj,
                  "billingprofile":billing_profile,
                  "login":login_form,
                  "guest_form":guest_form,
                  "address_qs":address_qs,
                  #"billing_address_form":billing_address_form,
                  "address_form":address_form #This is for the shipping above is for the billing address
            }
      return render(request,"carts/checkout.html",context)


def checkout_done_view(request):
      return render(request,"carts/checkout-done.html",{})
 
