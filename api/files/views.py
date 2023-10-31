from rest_framework import generics

from .models import Chunk, UploadedFile
from .serializers import ChunkSerializer, UploadedFileSerializer


class UploadedFileListCreateView(generics.ListCreateAPIView):
    """View for listing and creating File objects."""

    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def perform_create(self, serializer):
        """
        Create a new File object with the provided data, including
        processing the file name and associating it with the current user.
        """

        name = serializer.validated_data.get('name')
        file = self.request.data.get('file')

        # add extension to file name
        file_extension = str(file).split('.')[-1]
        file_name = f'{name}.{file_extension}'

        # return default file name from file if name not provided
        if not name:
            file_name = str(file)

        return serializer.save(
            name=file_name,
            size=file.size,
            type=file_extension,
            user=self.request.user
        )


class ChunkListCreateView(generics.ListCreateAPIView):
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer
