from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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