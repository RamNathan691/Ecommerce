from django.contrib.auth import authenticate,login
from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm,RegisterForm

# Create your views here.
 
def contactpage(request):
    contact_form=ContactForm()
    return render(request,"contact/contactpage.html",{"form":contact_form})


def loginpage(request):
    login_form=LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password =login_form.cleaned_data.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('login/')
        else:
               pass
    return render(request,"auth/loginpage.html",{"form":login_form})

def registerpage(request):
    register_form=RegisterForm(request.POST or None)
    return render(request,"auth/register.html",{"form":register_form})

