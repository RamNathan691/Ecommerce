from django.urls import path
from . import views
from account.views import RegisterView,LoginView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    #path('', views.homepage,name="homepage"),
    path('contact/',views.contactpage,name="contact"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('register/',RegisterView.as_view(),name="register"),
    path('register/guest',views.guest_page,name="guest")
    
]
