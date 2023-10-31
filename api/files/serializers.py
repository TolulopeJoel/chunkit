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
    Serializer for Chunk model
    """
    uploaded_file = UploadedFileSerializer(read_only=True)
    chunk_file = serializers.SerializerMethodField()
    position = serializers.IntegerField(read_only=True)

    class Meta:
        model = Chunk
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        uploaded_file_id = request.data.get('uploaded_file_id')

        if uploaded_file_id:
            try:
                uploaded_file = UploadedFile.objects.get(id=uploaded_file_id)

                # temporary solution to chunk file
                validated_data['uploaded_file'] = uploaded_file

                chunk_obj = Chunk(**validated_data)

                # TODO: Add support for other file types
                chunked_files = split_image(chunk_obj)

                for i, j in enumerate(chunked_files):
                    upload_data = cloudinary.uploader.upload(j)

                    validated_data['chunk_file'] = upload_data['secure_url']
                    validated_data['position'] = i + 1

                    last_chunk = Chunk(**validated_data)
                    last_chunk.save()

                return last_chunk
            except UploadedFile.DoesNotExist:
                raise serializers.ValidationError(
                    {"detail": "The provided uploaded file could not be found."}
                )
            except ValueError:
                raise serializers.ValidationError(
                    {"detail": "Invalid data provided."}
                )

        raise serializers.ValidationError(
            {"detail": "Failed to create a chunk. Upload a file."}
        )

    def get_chunk_file(self, object):
        request = self.context.get('request')
        file = object.chunk_file

        if file is not None:
            return request.build_absolute_uri(file.url)
