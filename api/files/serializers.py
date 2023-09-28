from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import File


class FileSerializer(serializers.ModelSerializer):
    """
    Serializer for File model
    """
    user = UserSerializer(read_only=True)
    # Changing the serializer field to FileField to ensure the API can accept files of any type
    # without encountering errors.
    file = serializers.FileField()

    class Meta:
        model = File
        fields = '__all__'
