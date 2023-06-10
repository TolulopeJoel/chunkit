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
