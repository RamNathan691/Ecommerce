from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signals import object_viewed_signal
from .utils import get_client_ip
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save,post_save
from account.signals import user_logged_in
User=settings.AUTH_USER_MODEL
class ObjectViewed(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#evenif the user isnt logged in you must be able to capture the data
    ip_address=models.CharField(max_length=200,blank=True,null=True)#there is an IPFIELD IN DJANGO but we are currently using the charfield
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)#it is for what model is it a product ,order,cart
    object_id=models.PositiveIntegerField()#used to get the current instance.id of the model that we are looking
    content_object=GenericForeignKey('content_type','object_id')#used get the whole instance info
    timestamp=models.DateTimeField(auto_now_add=True)#it is used for on which item which kind of things are bieng used or seen by the customer

    def __str__(self):
        return "%s viewed %s" %(self.content_object,self.timestamp)
    class Meta:
        ordering=['-timestamp']#it is for showing the most recent data
        verbose_name='Object viewed'
        verbose_name_plural='objects viewed'
def object_viewed_reciever(sender,instance,request,*args,**kwargs):
    c_type=ContentType.objects.get_for_model(sender)#instance.__class__
  #  print(sender)
   # print(instance)
    #print(request)
    #print(request.user)
    new_view_obj=ObjectViewed.objects.create(
        user=request.user,
        Content_type=c_type,
        object_id=instance.id,
        ip_address = get_client_ip(request)


    )
object_viewed_signal.connect(object_viewed_reciever)


class UserSession(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)#evenif the user isnt logged in you must be able to capture the data
    ip_address=models.CharField(max_length=200,blank=True,null=True)#there is an IPFIELD IN DJANGO but we are currently using the charfield
    timestamp=models.DateTimeField(auto_now_add=True)#it is used for on which item which kind of things are bieng used or seen by the customer
    session_key=models.CharField(max_length=100,null=True,blank=True)
    active=models.BooleanField(default=True)
    ended=models.BooleanField(default=False)

    def end_session(self):
        session_key=self.session_key
        ended=self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active=False
            self.ended=True
            self.save()
        except:
            pass
        return self.ended

#def post_save_session_reciever(sender,instance,created,*args,**kwargs):
 #   if created:
  #      qs=UserSession.objects.filter(user=instance.user,ended=False,active=False).exclude(id=instance.id)
   #     for i in qs:
    #        i.end_session()  
    #if not instance.active and not instance.ended:
     #   instance.end_session() 
#it ends all the session that is currently bieng active at that moment
#post_save.connect(post_save_session_reciever,sender=UserSession)


#def post_save_user_changed_reciever(sender,instance,created,*args,**kwargs):
 #   if not created:
  #      if instance.is_active == False:
   #         qs=UserSession.objects.filter(user=instance.user,ended=False,active=False)
    #        for i in qs:
     #           i.end_session()
#post_save.connect(post_save_user_changed_reciever,sender=User)

def user_logged_in_reciever(sender,instance,request,*args,**kwargs):
    user=instance
    ip_address=get_client_ip(request)
    session_key=request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key

    )
user_logged_in.connect(user_logged_in_reciever)