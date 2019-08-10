from django.shortcuts import render
from .forms import ContactForm
# Create your views here.
 
def contactpage(request):
    contact_form=ContactForm()
    return render(request,"contact/contactpage.html",{"form":contact_form})