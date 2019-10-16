from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save
User=settings.AUTH_USER_MODEL
# Create your models here.
import stripe
stripe.api_key="sk_test_2GsGy0BJZie3PWJQfSXWUOzF00TCAcAgtr"
#an email can have 10000 billing profile
#but an user should have only one billing profile
class Billingprofile(models.Model):
    user=models.OneToOneField(User,unique=True,null=True,blank=True,on_delete=models.CASCADE)
    email=models.EmailField()
    active=models.BooleanField(default=True)#we are having this active because we can have morethan or any number of billing profile to an email but when a user loggged in with that billing profile you should have only one billing profiles
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    customer_id=models.CharField(max_length=120,null=True,blank=True)
    def __str__(self):
        return self.email

def billing_profile_created_receiver(sender,instance,*args,**kwargs):
    if not instance.customer_id and instance.email:
        print("ACTUAL API REQUEST SENT TO THE STRIPE")
        customer=stripe.Customer.create(
                email=instance.email
        )
        instance.customer_id=customer.id
pre_save.connect(billing_profile_created_receiver,sender=Billingprofile)

def user_created_reciever(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        Billingprofile.objects.get_or_create(user=instance,email=instance.email)
#whenever an user is created it is used to create an  billing for that user
post_save.connect(user_created_reciever,sender=User)

#sender is important in the signals as the User is created it is moved to the