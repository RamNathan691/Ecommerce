from django import forms
from django.contrib.auth import get_user_model
User=get_user_model()
class ContactForm(forms.Form):
    fullname = forms.CharField(widget = forms.TextInput(attrs={'class':"form-control","placeholder":"Enter your name"}))
    email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your emial adress',}))
    content = forms.CharField(widget = forms.Textarea
    (attrs={'class':'form-control','placeholder':'Please Enter Your queries here :)'}))

   
class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the USERNAME'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class RegisterForm(forms.Form):
        username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter the USERNAME'}))
        email = forms.EmailField(widget = forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your emial adress',}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
        confirmpassword = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
        
        def clean_username(self):    
            username=self.cleaned_data.get('username')
            qs=User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError("Username is taken already")
            return username

        def clean(self):
            data=self.cleaned_data
            
            password1=self.cleaned_data.get('password')
            cnfpassword=self.cleaned_data.get('confirmpassword')

            if password1 != cnfpassword:
                raise forms.ValidationError("Password Mismatch")
            if len(password1) < 10:
                raise forms.ValidationError("Your Password length is too short")
            return data

            
           



















