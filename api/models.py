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
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS, default="1")
    priority = models.CharField(max_length=1, choices=PRIORITY, default="1")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True, help_text="Must be greater than created and updated date.")

    def clean(self):
        if self.due_date:
            # Ensure due_date is after created_at and updated_at
            if self.due_date <= self.created_at or self.due_date <= self.updated_at:
                raise ValidationError('Due date must be after the creation and last update date.')
        
        # Override the save method to call clean()
    def save(self, *args, **kwargs):
        self.clean()  # Call clean method before saving
        super().save(*args, **kwargs)
        
    
    def update_status(self):
        if self.status == "1":
            self.status = "2"
        elif self.status == "2":
            self.status = "3"
        else:
            raise ValidationError("Cannot assign the status")

    def __str__(self):
        return self.title