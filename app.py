import os

from chunkers import image_split, text_split, video_split, pdf_split, archive_split

file_extensions = {
    'image': ['.jpg', '.jpeg', '.png', '.webp', '.svg', '.gif', '.bmp', '.ico', '.tiff'],
    'archive': ['.tar', '.gz', '.zip', '.rar', '.7z'],
    'video': ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.m4v'],
    'audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'document': ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx'],
    'text': ['.txt', '.csv'],
    'pdf': ['.pdf'],
}

file_handlers = {
    "image": image_split,
    "archive": archive_split,
    "video": video_split,
    "text": text_split,
    "pdf": pdf_split,
}


def get_file_extension(file):
    file_basename = os.path.basename(file)
    file_pathname = os.path.splitext(file_basename)
    file_extension = file_pathname[1]

    return file_extension


def get_file_type(file_path):
    file_extension = get_file_extension(file_path)

    for extension_type, extensions in file_extensions.items():
        if file_extension in extensions:
            return extension_type

    return None


def handle_file(file):
    file_type = get_file_type(file)
    
    if file_type:
        handler_func = file_handlers.get(file_type)
        print(handler_func(file))
    else:
        return "Unsupported file type"

