import concurrent.futures
import shutil

import cloudinary
from rest_framework.views import Response, status

from ..models import Chunk, UploadedFile
from ..serializers import ChunkSerializer, UploadedFileSerializer
from ..utils import error_response, get_folder_path, success_response
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


def get_file_splitter(file_object: UploadedFile) -> function | None:
    """
    Returns the appropriate file splitting function based uploaded file type
    """
    return next(
        (
            FILE_HANDLERS.get(extension_type)
            for extension_type, extensions in FILE_EXTENSIONS.items()
            if file_object.type in extensions
        ),
        None,
    )


def split_uploaded_file(uploaded_file_id: int, validated_data: dict, num_chunks: int) -> Response:
    """
    Splits uploaded file into chunks and upload them to cloudinary.
    """
    uploaded_file = UploadedFile.objects.filter(id=uploaded_file_id).first()

    validated_data["uploaded_file"] = uploaded_file
    splitter = get_file_splitter(uploaded_file)
    chunked_files = splitter(uploaded_file, num_chunks)

    if isinstance(chunked_files, str):
        return error_response(f"Can't create chunk. {chunked_files}.")

    created_chunks = set()
    if has_old_chunks(uploaded_file):
        # logic to create muliple chunks at once
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    process_chunk, validated_data, index, file, created_chunks
                )
                for index, file in enumerate(chunked_files)
            ]
            concurrent.futures.wait(futures)

    data = {
        "uploaded_file": UploadedFileSerializer(uploaded_file).data,
        "chunks": ChunkSerializer(created_chunks, many=True).data
    }
    return success_response(data, status=status.HTTP_201_CREATED)


def process_chunk(validated_data: dict, index: int, file: __file__, created_chunks: set):
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

    yield chunk
    created_chunks.add(chunk)

    # remove chunk files from local filesystem
    shutil.rmtree(f"{validated_data["uploaded_file"].name}_chunks")


def has_old_chunks(uploaded_file: UploadedFile) -> bool:
    """
    This function checks if an UploadedFile has chunks, then deletes them.
    """
    try:
        chunks = uploaded_file.file_chunks.all()

        if chunks.exists():
            chunks.delete()
        return True
    except Exception:
        return False
