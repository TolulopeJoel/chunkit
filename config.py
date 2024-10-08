import os
from typing import Callable

from chunkers.archive_chunker import split_archive
from chunkers.image_chunker import split_image
from chunkers.pdf_chunker import split_pdf
from chunkers.text_chunker import split_text
from chunkers.video_chunker import split_video

# Conversation states
GET_FILE, GET_NUM_CHUNKS, CONFIRM_CHUNKS = range(3)
DEBUG = False

file_extensions = {
    "image": (".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".bmp", ".ico", ".tiff"),
    "video": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".m4v"),
    "archive": (".tar", ".gz", ".zip", ".rar", ".7z"),
    "text": (".txt", ".csv"),
    "pdf": (".pdf"),
}

file_handlers = {
    "image": split_image,
    "archive": split_archive,
    "video": split_video,
    "text": split_text,
    "pdf": split_pdf,
}


def get_split_function(file_path: str) -> Callable:
    """Get the appropriate split function based on file extension."""
    file_extension = os.path.splitext(file_path)[1].lower()
    return next(
        (
            file_handlers[extension_type]
            for extension_type, extensions in file_extensions.items()
            if file_extension in extensions
        ),
        None,
    )
