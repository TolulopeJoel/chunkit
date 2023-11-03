import shutil

import cloudinary
from rest_framework import serializers

from .models import Chunk, UploadedFile
from .services import split_image

from accounts.serializers import UserSerializer


class UploadedFileSerializer(serializers.ModelSerializer):
    """
    Serializer for File model
    """
    user = UserSerializer(read_only=True)
    file = serializers.FileField()

    class Meta:
        model = UploadedFile
        fields = '__all__'

    def get_file(self, object):
        request = self.context.get('request')
        file_url = object.file.url
        return request.build_absolute_uri(file_url)


class ChunkSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chunk model.
    """
    uploaded_file = UploadedFileSerializer(read_only=True)
    chunk_file = serializers.URLField(read_only=True)
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chunk
        fields = '__all__'
