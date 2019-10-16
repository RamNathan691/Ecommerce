from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
import stripe
from django.utils.http import is_safe_url
stripe.api_key="sk_test_2GsGy0BJZie3PWJQfSXWUOzF00TCAcAgtr"
STRIPE_PUB_KEY='pk_test_fG9TWih683sQBIqnZmitA9f800WJ06GXpE'
def payment_method_view(request):
    next_url=None
    next_=request.GET.get('next')
    if is_safe_url(next_,request.get_host()):
        next_url=next_
    return render(request,'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY,"next_url":next_url})

def payment_method_createview(request):
    if request.method =="POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message":"Success!Your card has been added"})
    return HttpResponse("Error",status_code=401)

