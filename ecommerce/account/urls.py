from django.urls import path
from . import views
urlpatterns = [
    #path('', views.homepage,name="homepage"),
    path('contact/',views.contactpage,name="contact"),
    path('login/',views.loginpage,name="login"),
    path('register/',views.registerpage,name="user")
    
]
