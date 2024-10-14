from rest_framework.serializers import ModelSerializer
from api.models import User
from rest_framework import serializers


class RegisterUserSerializer(ModelSerializer):
    password = serializers.CharField(max_length=20, write_only=True)
    confirm_password = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password']

    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Password Does Not Match!")
        return attrs


    def create(seld, validate_data):
        return User.objects.create_user(**validate_data)
    
