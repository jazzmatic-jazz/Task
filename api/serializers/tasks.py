from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import User, Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['assigned_to','created_at', 'title', 'description', 'status', 'priority', 'due_date']

        
