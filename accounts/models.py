from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import re
from django.core.exceptions import ValidationError

# Create your models here.
class User(AbstractUser):
    username= None
    email = models.EmailField(unique=True)
    forget_password_token= models.CharField(max_length=255,  null=True , blank=True)
    phone_number = models.CharField(
        verbose_name='Phone Number',
        help_text='Enter your phone number in international format (e.g., +1234567890).',
        null=True,
        blank=True,
        max_length=50
    )
    followers = models.ManyToManyField("self", blank=True)

    email_token = models.CharField(max_length=200, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    objects = CustomUserManager()
    # helllo 

    def __str__(self):
        return self.email

    def clean(self):
        super().clean()
    
    
   
    

