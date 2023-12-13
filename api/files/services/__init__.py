import concurrent.futures
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
    "image": ("jpg", "jpeg", "png", "webp", "svg", "gif", "bmp", "ico", "tiff"),
    "video": ("mp4", "mkv", "avi", "mov", "wmv", "flv", "m4v"),
    "archive": ("tar", "gz", "zip", "rar", "7z"),
    "text": ("txt", "csv"),
    "pdf": ("pdf",),
}

FILE_HANDLERS = {
    "image": split_image,
    "archive": split_archive,
    "video": split_video,
    "text": split_text,
    "pdf": split_pdf,
}


def get_file_splitter(file_object):
    """Determine and return the appropriate file splitting function based
    uploaded file type

    Args:
        file_object: An instance of UploadedFile representing the uploaded file

    Returns:
        callable or None: The file splitting function corresponding to the file type, or None if not found.
    """
    return next(
        (
            FILE_HANDLERS.get(extension_type)
            for extension_type, extensions in FILE_EXTENSIONS.items()
            if file_object.type in extensions
        ),
        None,
    )


def split_uploaded_file(
    uploaded_file_id, validated_data, num_chunks, created_chunks
):
    """Splits uploaded file into chunks and upload them to cloudinary

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

    uploaded_file = (
        UploadedFile.objects
        .filter(id=uploaded_file_id).first()
    )

    validated_data["uploaded_file"] = uploaded_file
    splitter = get_file_splitter(uploaded_file)
    chunked_files = splitter(uploaded_file, num_chunks)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_chunk, validated_data, index, file, created_chunks
            )
            for index, file in enumerate(chunked_files)
        ]
        concurrent.futures.wait(futures)

    shutil.rmtree(f"{uploaded_file.name}_chunks")

    data = {
        "status": "success",
        "message": "File successfully split into chunks.",
        "data": {
            "uploaded_file": UploadedFileSerializer(uploaded_file).data,
            "chunks": ChunkSerializer(created_chunks, many=True).data
        }
    }

    return Response(data, status=status.HTTP_201_CREATED)


def process_chunk(validated_data, index, file, created_chunks):
    """
    This function handles each chunk processing
    """
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
