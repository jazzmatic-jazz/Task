from django.contrib import admin
from .models import User, Task

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', "name", "is_active", "is_staff"]


class TaskAdmin(admin.ModelAdmin):
    list_display = ["assigned_to", "title", "description"]
    
admin.site.register(User, UserAdmin)
admin.site.register(Task)
