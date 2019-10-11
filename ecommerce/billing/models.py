from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
User=settings.AUTH_USER_MODEL
# Create your models here.
import stripe
stripe.api_key="sk_test_2GsGy0BJZie3PWJQfSXWUOzF00TCAcAgtr"

class Billingprofile(models.Model):
    user=models.OneToOneField(User,unique=True,null=True,blank=True,on_delete=models.CASCADE)
    email=models.EmailField()
    active=models.BooleanField(default=True)#we are having this active because we can have morethan or any number of billing profile to an email but when a user loggged in with that billing profile you should have only one billing profiles
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    customer_id=models.CharField(max_length=120,null=True,blank=True)
    def __str__(self):
        self.email

def user_created_reciever(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        Billingprofile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_reciever,sender=User)