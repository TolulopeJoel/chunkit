from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Chunk, UploadedFile


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
    Serializer for Chunk model
    """
    uploaded_file = UploadedFileSerializer(read_only=True)
    chunk_file = serializers.SerializerMethodField()

    class Meta:
        model = Chunk
        fields = '__all__'

    def get_chunk_file(self, object):
        request = self.context.get('request')
        file_url = object.chunk_file.url
        return request.build_absolute_uri(file_url)
