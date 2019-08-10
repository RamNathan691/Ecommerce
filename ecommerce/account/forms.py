from django import forms

class ContactForm(forms.Form):
    fullname=forms.CharField(widget=forms.TextInput(attrs={'class':"form-control","placeholder":"Enter your name"}))
    email= forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your emial adress',}))
    content=forms.CharField(widget=forms.Textarea
    (attrs={'class':'form-control','placeholder':'Please Enter Your queries here :)'}))