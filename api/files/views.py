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
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer
