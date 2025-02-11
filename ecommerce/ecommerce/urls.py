"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include 
from django.conf import settings
from django.conf.urls.static import static
from address.views import checkout_address_create_view,checkout_address_reuse_view
from cart.views import cart_detail_api_view
from billing.views import payment_method_view,payment_method_createview
#so basically U shouldnt use the staticfiles as such done in this project while deployment
urlpatterns = [
    
    path('',include('account.urls')),
    path('carts/',include('cart.urls')),
    path('products/',include('products.urls')),
    path('search/',include('search.urls')),
    path('admin/', admin.site.urls),
    path('billing/payment-method/',payment_method_view,name='payment'),
    path('payment-create-method/',payment_method_createview,name='payment-create'),
    path('checkout/address/create/view/',checkout_address_create_view,name="checkoutaddress"),
    path('checkout/address/resuse/',checkout_address_reuse_view,name="checkoutreuse")
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static (settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    