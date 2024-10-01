from archive_chunker import split_archive
from image_chunker import split_image
from pdf_chunker import split_pdf
from text_chunker import split_text
from video_chunker import split_video

# Conversation states
GET_FILE, GET_NUM_CHUNKS, CONFIRM_CHUNKS = range(3)

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
