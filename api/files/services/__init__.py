import concurrent.futures
import os
import shutil

import cloudinary
from rest_framework.views import Response, status

from ..models import Chunk, UploadedFile
from ..serializers import ChunkSerializer, UploadedFileSerializer
from ..utils import get_folder_path
from .archive_services import split_archive
from .image_services import split_image
from .pdf_services import split_pdf
from .text_services import split_text
from .video_services import split_video

FILE_EXTENSIONS = {
    "image": (".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".bmp", ".ico", ".tiff"),
    "video": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".m4v"),
    "archive": (".tar", ".gz", ".zip", ".rar", ".7z"),
    "text": (".txt", ".csv"),
    "pdf": (".pdf"),
}

FILE_HANDLERS = {
    "image": split_image,
    "archive": split_archive,
    "video": split_video,
    "text": split_text,
    "pdf": split_pdf,
}


def get_split_function(file_path):
    file_extension = os.path.splitext(file_path)[1]

    return next(
        (
            FILE_HANDLERS.get(extension_type)
            for extension_type, extensions in FILE_EXTENSIONS.items()
            if file_extension in extensions
        ),
        None,
    )




def split_uploaded_file(
    uploaded_file_id: int,
    validated_data: dict,
    num_chunks: int,
    created_chunks: list,
) -> Response:
    """Split an uploaded file into multiple chunks and upload them to a cloud
    storage service.

    Args:
        uploaded_file_id (int): The ID of the uploaded file.
        validated_data (dict): The validated data for creating the chunks.
        num_chunks (int): The number of chunks to split the file into.
        created_chunks (list): A list to store the created chunk objects.

    Returns:
        Response: A response object containing the serialized data
        of the created chunk objects.

    Raises:
        DoesNotExist: If the uploaded file with the given ID does not exist.
    """

    validated_data["uploaded_file"] = UploadedFile.objects.get(
        id=uploaded_file_id
    )

    # TODO: Add support for other file types
    chunk_obj = Chunk(**validated_data)
    chunked_files = split_image(chunk_obj, num_chunks)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_chunk, validated_data, index, file, created_chunks
            )
            for index, file in enumerate(chunked_files)
        ]
        concurrent.futures.wait(futures)

    shutil.rmtree(f"{chunk_obj.uploaded_file.name}_chunks")

    response_data = {
        "uploaded_file": UploadedFileSerializer(chunk_obj.uploaded_file).data,
        "chunk_files": ChunkSerializer(created_chunks, many=True).data
    }

    return Response(
        response_data,
        status=status.HTTP_201_CREATED,
    )


def process_chunk(validated_data, index, file, created_chunks):
    """This function handles each chunk processing"""
    upload_data = cloudinary.uploader.upload(
        file,
        resource_type="auto",
        folder=get_folder_path("file_chunks"),
    )

    validated_data["chunk_file"] = upload_data["secure_url"]
    validated_data["position"] = index + 1

    chunk = Chunk(**validated_data)
    chunk.save()
    created_chunks.append(chunk)
