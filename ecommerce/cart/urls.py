from django.urls import path,include 
from .views import cart_home,cart_update
urlpatterns = [
  
    path('carthome',cart_home, name= "carthome"),
    path('update',cart_update, name= "cartupdate"),
]