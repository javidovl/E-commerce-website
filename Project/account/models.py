from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.contrib.auth import get_user_model
from django.contrib.auth.models import UserManager
from django_countries.fields import CountryField




class UserManager(UserManager):

    def create_user(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user 





class User(AbstractBaseUser, PermissionsMixin):
    name=models.CharField(max_length=128, null=True, blank=True)
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=128)
    is_staff = models.BooleanField(default=False)
    nickname=models.CharField(max_length=255, default=None, blank=True, null=True)
    is_active=models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email
    
    def get_nickname(self):
        return self.nickname

    objects = UserManager()



class BillingAddress(models.Model):
    billing_address_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="billing_address_of_user")
    billing_address_first_name=models.CharField(max_length=50)
    billing_address_last_name=models.CharField(max_length=50)
    billing_address_email=models.EmailField()
    billing_address_country=CountryField(blank_label='(select country)')
    billing_address_address=models.CharField(max_length=100)
    billing_address_mobile_phone=models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.billing_address_user.email} - {self.billing_address_first_name}"