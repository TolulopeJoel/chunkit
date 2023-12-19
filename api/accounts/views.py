from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from .permissions import IsSuperUser

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView to include user email.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser, permissions.IsAdminUser]


class SignUpView(generics.CreateAPIView):
    """
    View to register new users.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
