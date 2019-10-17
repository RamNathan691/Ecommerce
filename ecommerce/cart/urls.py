from django.urls import path,include 
from .views import cart_home,cart_update,checkout_home,cart_detail_api_view,checkout_done_view
urlpatterns = [
  
    path('carthome',cart_home, name= "carthome"),
    path('update',cart_update, name= "cartupdate"),
    path('checkout',checkout_home, name= "checkout"),
    path('api/cart/',cart_detail_api_view, name= "apiview"),
    path('success/',checkout_done_view,name='success'),


]