from django.shortcuts import render
from .forms import ContactForm,LoginForm
# Create your views here.
 
def contactpage(request):
    contact_form=ContactForm()
    return render(request,"contact/contactpage.html",{"form":contact_form})


def loginpage(request):
    login_form=LoginForm(request.POST or None)
    if login_form.is_valid():
        pass
    return render(request,"auth/loginpage.html",{"form":login_form})

def registerpage(request):
    return render(request,"auth/register.html",{})