from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,BaseUserManager
)
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,email,password=None,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        user=self.model(
            email=self.normalize_email(email)

        )
        user.set_password(password)#it is also used to change the user password
        user.save(using=self._db)
        return user_obj



class GuestEmail(models.Model):
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
     return self.email

class User(AbstractBaseUser):
    email=models.EmailField(max_length=255,unique=True)
    active=models.BooleanField(default=True)# can login
    staff=models.BooleanField(default=False)# staff user non superuser
    admin=models.BooleanField(default=False)# superuser
    timestamp=models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD='email'#this is the goona be the default username
    objects=UserManager()
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email 
     

    
    @property
    
    def is_staff(self):
        return self.staff
    
    @property
    
    def is_admin(self):
        return self.admin
    
    @property
    
    def is_active(self):
        return self.active