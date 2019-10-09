from django.db import models
from django.contrib.auth.models import(
    AbstractBaseUser,BaseUserManager
)
# Create your models here.
class UserManager(BaseUserManager):
    #normal user
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Enter the Password")
        user_obj=self.model(
            email=self.normalize_email(email)

        )
        user_obj.set_password(password)#it is also used to change the user password
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj
        #i do known what is staffuser for 
    def create_staffuser(self,email,password=None):
        user=self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return user
        #creating the superuser
    def create_superuser(self,email,password=None):
            user=self.create_user(
              email,
              password=password,
              is_admin=True,
              is_staff=True
              )
            return user#basically he is also a staff user



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
    FirstName=models.CharField(max_length=280,blank=True,null=True)
    LastName=models.CharField(max_length=280,blank=True,null=True)
    USERNAME_FIELD='email'#this is the goona be the default username
    objects=UserManager()
    #Username_filed and passsword are required by default
    REQUIRED_FIELDS=[]#this is used to add the additional required fields this are used only when like python manage.py createsuperuser
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email 
     #these methods are called the built-in methods
    #so for the module_perm error these are the method to overcome this
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    
    @property
    
    def is_staff(self):
        return self.staff
    
    @property
    
    def is_admin(self):
        return self.admin
    
    @property
    
    def is_active(self):
        return self.active