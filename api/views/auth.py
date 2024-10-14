from api.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from api.serializers.auth import RegisterUserSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


def create_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterAPI(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"status": "success", "msg": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "msg": "Failed to create user."}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"status": "error", "msg": "email or password cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)

        if not user:
            return Response({"status": "error", "msg": "Not a valid user"}, status=status.HTTP_400_BAD_REQUEST)
    
        token = create_token(user)
        return Response({"status": "success", "message": "Login Successfully", "token": token}, status=status.HTTP_200_OK)
        