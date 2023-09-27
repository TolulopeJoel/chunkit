from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from .serializers import UserSerializer


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
