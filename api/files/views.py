from rest_framework import generics

from .models import File
from .serializers import FileSerializer


class FileListCreateView(generics.ListCreateAPIView):
    """View for listing and creating File objects."""

    queryset = File.objects.all()
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        """
        Create a new File object with the provided data, including
        processing the file name and associating it with the current user.
        """

        name = serializer.validated_data.get('name')
        file = str(self.request.data.get('file'))

        # add extension to file name
        file_extension = file.split('.')[-1]
        file_name = f'{name}.{file_extension}'

        # return default file name from file if name not provided
        if not name:
            file_name = str(file)

        return serializer.save(name=file_name, user=self.request.user)
