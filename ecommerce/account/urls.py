from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    #path('', views.homepage,name="homepage"),
    path('contact/',views.contactpage,name="contact"),
    path('login/',views.loginpage,name="login"),
     path('logout/',LogoutView.as_view(),name="logout"),
    path('register/',views.registerpage,name="register"),
    path('register/guest',views.guest_page,name="guest")
    
]
