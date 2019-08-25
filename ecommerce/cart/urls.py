from django.urls import path,include 
from .views import cart_home,cart_update
urlpatterns = [
  
    path('',cart_home, name= "carthome"),
    path('update',cart_update, name= "cartupdate"),
]