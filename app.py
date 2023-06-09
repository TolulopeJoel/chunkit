import os

from chunkers import image_split, text_split, video_split, pdf_split, archive_split

file_extensions = {
    'image': ['.jpg', '.jpeg', '.png', '.webp', '.svg'],
    'archive': ['.tar', '.gz', '.zip'],
    'video': ['.mp4', '.mkv'],
    'text': ['.txt'],
    'pdf': ['.pdf'],
}
