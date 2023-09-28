from rest_framework import generics

from .models import File
from django.contrib.auth import get_user_model
from .serializers import FileSerializer


class FileListCreateView(generics.ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
