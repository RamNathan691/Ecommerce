from django.shortcuts import render
import stripe
stripe.api_key="sk_test_2GsGy0BJZie3PWJQfSXWUOzF00TCAcAgtr"
STRIPE_PUB_KEY='pk_test_fG9TWih683sQBIqnZmitA9f800WJ06GXpE'
def payment_method_view(request):
    if request.method =="POST":
        print(request.POST)
    return render(request,'billing/payment-method.html',{"publish_key":STRIPE_PUB_KEY})
