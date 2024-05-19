from rest_framework import generics
from rest_framework.views import status

from .models import Chunk, UploadedFile
from .serializers import ChunkSerializer, UploadedFileSerializer
from .services import split_uploaded_file
from .utils import error_response, success_response


class UploadedFileListCreateView(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def perform_create(self, serializer):
        # proccess the file name
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


class ChunkCreateView(generics.CreateAPIView):
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer

    def create(self, request, *args, **kwargs):
        uploaded_file_id = request.data.get('uploaded_file_id')
        num_chunks = request.data.get('num_chunks') or 2

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        if uploaded_file_id:
            try:
                return split_uploaded_file(uploaded_file_id, validated_data, int(num_chunks))
            except UploadedFile.DoesNotExist as exception:
                return error_response(message=str(exception), status=status.HTTP_404_NOT_FOUND)
            except (ValueError, SystemError) as exception:
                return error_response(str(exception))

        return error_response("Failed to create a chunk. Upload a valid file.")


class ChunkListView(generics.ListAPIView):
    queryset = Chunk.objects.all()
    serializer_class = ChunkSerializer

    def list(self, request, *args, **kwargs):
        """
        Retrieves a list of chunks associated with an uploaded file.
        """
        file_id = kwargs['file_id']
        uploaded_file = UploadedFile.objects.filter(
            id=file_id, user=self.request.user).first()

        if uploaded_file:
            chunks = uploaded_file.file_chunks.all()

            return success_response({
                "uploaded_file": UploadedFileSerializer(uploaded_file).data,
                "chunks": ChunkSerializer(chunks, many=True).data
            })

        return error_response(message="Uploaded file not found", status=status.HTTP_404_NOT_FOUND)
