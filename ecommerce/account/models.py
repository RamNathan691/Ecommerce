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
        user=self.model(
            email=self.normalize_email(email)

        )
        user.set_password(password)#it is also used to change the user password
        user.staff=is_staff
        user.admin=is_admin
        user.active=active
        user.save(using=self._db)
        return user
        #i do known what is staffuser for 
    def create_staffuser(self,email,password=None):
        staff_user=self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return staff_user
        #creating the superuser
        def create_superuser(self,email,password=None):
            staff_user=self.create_user(
            email,
            password=password,
            is_admin=True,
            is_staff=True,#basically he is also a staff user
        )
        return staff_user



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
    #Username_filed and passsword are required by default
    REQUIRED_FIELDS=[]#this is used to add the additional required fields this are used only when like python manage.py createsuperuser
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