import shutil

import cloudinary
from rest_framework import generics
from rest_framework.views import Response, status

from .models import Chunk, UploadedFile
from .serializers import ChunkSerializer, UploadedFileSerializer
from .services import split_image


class UploadedFileListCreateView(generics.ListCreateAPIView):
    """View for listing and creating File objects."""

    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def perform_create(self, serializer):
        """
        Create a new File object with the provided data, including
        processing the file name and associating it with the current user.
        """

        file = self.request.data.get('file')
        f = str(file).split('.')
        file_extension = f[-1]
        file_name = serializer.validated_data.get('name') or ''.join(f[:-1])

        return serializer.save(
            name=file_name,
            size=file.size,
            type=file_extension,
            user=self.request.user
        )


class ChunkListCreateView(generics.ListCreateAPIView):
    """
    A view for listing and creating Chunk instances.
    """

    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer

    def create(self, request, *args, **kwargs):
        """
        Creates a chunk by splitting an uploaded file into smaller parts and
        saving them as Chunk model instances.

        Returns:
            A response containing the serialized representation of the created chunks.

        Raises:
            ValueError: If invalid data is provided.
            UploadedFile.DoesNotExist: If the provided uploaded file could not be found.
        """

        uploaded_file_id = request.data.get('uploaded_file_id')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if uploaded_file_id:
            created_chunks = []  # List to store created chunks

            try:
                validated_data['uploaded_file'] = UploadedFile.objects.get(
                    id=uploaded_file_id
                )

                # TODO: Add support for other file types
                chunk_obj = Chunk(**validated_data)
                chunked_files = split_image(chunk_obj, 4)

                for i, j in enumerate(chunked_files):
                    upload_data = cloudinary.uploader.upload(j)

                    validated_data['chunk_file'] = upload_data['secure_url']
                    validated_data['position'] = i + 1

                    chunk = Chunk(**validated_data)
                    chunk.save()
                    created_chunks.append(chunk)

                # delete chunk folder on local storage
                shutil.rmtree(f"{chunk.uploaded_file.name}_chunks")

                return Response(
                    ChunkSerializer(created_chunks, many=True).data,
                    status=status.HTTP_201_CREATED
                )
            except UploadedFile.DoesNotExist:
                return Response(
                    {"detail": "The provided uploaded file could not be found."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ValueError:
                return Response(
                    {"detail": "Invalid data provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"detail": "Failed to create a chunk. Upload a file."},
            status=status.HTTP_400_BAD_REQUEST
        )
