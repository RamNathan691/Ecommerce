from django.contrib.auth import authenticate,login,get_user_model
from django.shortcuts import render,redirect
from .forms import ContactForm,LoginForm,RegisterForm,GuestForm
from django.contrib import messages
from django.utils.http import is_safe_url
from .models import GuestEmail
from django.views.generic import CreateView,FormView
from django.http import JsonResponse,HttpResponse
# Create your views here.
from .signals import user_logged_in
User=get_user_model()
def contactpage(request):
    contact_form=ContactForm()
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({"messsage" : "Thank You"})
    if contact_form.errors:
        errors=contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type='application/json')
    return render(request,"contact/contactpage.html",{"form":contact_form})
#guest page hhas only the email field to be get
def guest_page(request):
    guest_form=GuestForm(request.POST or None)
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if guest_form.is_valid():
        email=guest_form.cleaned_data.get("email")
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
        else:
             return redirect("register")
    return redirect("register")
class LoginView(FormView):
      form_class=LoginForm
      success_url='/products/'
      template_name="auth/loginpage.html"

      def form_valid(self,form):
        request=self.request
        next_=request.GET.get('next')
        next_post=request.POST.get('next')
        redirect_path=next_ or next_post or None
        username = form.cleaned_data.get("username")
        password =form.cleaned_data.get("password")
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)  
            user_logged_in.send(user.__class__,instance= user,request=request)
            try:
                del request.session['guest_email']
            except:
                    pass
            if is_safe_url(redirect_path,request.get_host()):
                print(redirect_path)
                return redirect(redirect_path)
                #return messages.error(redirect_path+"Wrong Navigation")
            else:
                   return redirect('products')
        return super(LoginView,self).form_invalid(form)

#def loginpage(request):
 #   login_form=LoginForm(request.POST or None)
  #  next_=request.GET.get('next')
   # next_post=request.POST.get('next')
    #redirect_path=next_ or next_post or None
   # if login_form.is_valid():
    #    username = login_form.cleaned_data.get("username")
     #   password =login_form.cleaned_data.get("password")
      #  user = authenticate(request,username=username,password=password)
       # print(user)
        #if user is not None:
         #   login(request,user)  
          #  try:
           #     del request.session['guest_email']
            #except:
             #       pass
            #if is_safe_url(redirect_path,request.get_host()):
             #   return redirect(redirect_path)
            #else:
             #      messages.success(request,("Invalid Login Navigation "))
        #else:
         #     messages.success(request,("Your username is not valid"))
    #return render(request,"auth/loginpage.html",{"form":login_form})

class RegisterView(CreateView):
    form_class=RegisterForm
    template_name='auth/register.html'
    success_url='/login/'

#def registerpage(request):
#    register_form=RegisterForm(request.POST or None)
 #   if register_form.is_valid():
  #      username = register_form.cleaned_data.get("username")
   #     password = register_form.cleaned_data.get("password") 
    #    email = register_form.cleaned_data.get("email")
     #   news_uesr=User.objects.create_user(username,email,password)
    #return render(request,"auth/register.html",{"form":register_form})

