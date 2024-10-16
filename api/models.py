from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from .choices import PRIORITY, STATUS
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


class User(AbstractBaseUser, PermissionsMixin):
    '''
        Custom user using AbstractBaseUser where we use
        email field as the main field for creating user
    '''
    email = models.EmailField(max_length=255,unique=True)    
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email
    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_created_by')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default="1")
    priority = models.CharField(max_length=1, choices=PRIORITY, default="1")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    due_date = models.DateField(null=True, blank=True, help_text="Must be greater than created and updated date.")

   

    def __str__(self):
        return self.title