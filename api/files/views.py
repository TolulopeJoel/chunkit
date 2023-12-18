from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView
from rest_framework.views import Response, status

from .models import Chunk, UploadedFile
from .serializers import ChunkSerializer, UploadedFileSerializer
from .services import split_uploaded_file


class UploadedFileListCreateView(ListCreateAPIView):
    """
    View for listing and creating File objects.
    """
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

    def get_queryset(self):
        user = self.request.user
        return super().get_queryset().filter(user=user)


class ChunkCreateView(CreateAPIView):
    """
    A view for creating Chunk instances.
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
        num_chunks = request.data.get('num_chunks') or 2

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if uploaded_file_id:
            try:
                return split_uploaded_file(
                    uploaded_file_id, validated_data, num_chunks
                )

            except UploadedFile.DoesNotExist:
                return Response(
                    {"detail": "The provided uploaded file could not be found."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            except (ValueError, SystemError):
                return Response(
                    {"detail": "Invalid data provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(
            {"detail": "Failed to create a chunk. Upload a file."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ChunkListView(ListAPIView):
    """
    A view for retrieving a list of chunks associated with an uploaded file.
    """
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of chunks associated with an uploaded file.

        Explanation:
        This function retrieves the chunks associated with an uploaded file identified
        by the file ID provided in the URL parameters.

        Returns:
        - A response with the serialized data of the uploaded file and its associated chunks if file is found.
        """
        file_id = kwargs['file_id']
        uploaded_file = UploadedFile.objects.filter(
            id=file_id, user=self.request.user).first()

        if uploaded_file:
            chunks = uploaded_file.file_chunks.all()

            data = {
                "status": "success",
                "data": {
                    "uploaded_file": UploadedFileSerializer(uploaded_file).data,
                    "chunks": ChunkSerializer(chunks, many=True).data
                }
            }

            return Response(data, status=status.HTTP_200_OK)
        return Response({"detail": "Uploaded file not found"}, status=status.HTTP_404_NOT_FOUND)
