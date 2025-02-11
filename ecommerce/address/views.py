from django.shortcuts import render,redirect
from .forms import AddressForm
from django.contrib import messages
from django.utils.http import is_safe_url
from billing.models import Billingprofile
from .models import Address
# Create your views here.
def checkout_address_create_view(request):
    user=request.user
    form=AddressForm(request.POST or None)
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if form.is_valid():
          instance=form.save(commit=False)
          if user.is_authenticated:
            billing_profile,billing_profile_created = Billingprofile.objects.get_or_create(user=user,email=user.email)                         
            if billing_profile is not None:
                addressType = request.POST.get('addressType','shipping')
                instance.billing_profile = billing_profile
                instance.addressType = addressType
                instance.save()
                request.session[addressType+"_address_id"]=instance.id
                print(addressType)
                
       
          else:
                  messages.success(request,("Error the address is not saved or Pls LoginIn to continue :( "))
                  return redirect("checkout")
          if is_safe_url(redirect_path,request.get_host()):
              return redirect(redirect_path)
          else:
              return redirect("checkout")
    return redirect("checkout")


def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        user=request.user
        context={}
        next_=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path=next_ or next_post or None
        if request.method=='POST':#there is no instance we are getting it in the request.method
            shipping_address=request.POST.get("shipping_address",None)
            addressType = request.POST.get('addressType','shipping')
            billing_profile,billing_profile_created = Billingprofile.objects.get_or_create(user=user,email=user.email)                          
            print(addressType)
            if shipping_address is not None:
                qs=Address.objects.filter(billing_profile=billing_profile,id=shipping_address)
                if qs.exists():
                    request.session[addressType+"_address_id"]=shipping_address
            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:
                  return redirect("checkout")
    return redirect("checkout")







     