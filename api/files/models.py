from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from .utils import get_folder_path


class UploadedFile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )
    file = CloudinaryField(
        folder=get_folder_path("uploaded_files"),
        resource_type='auto'
    )
    name = models.CharField(max_length=255, blank=True, null=False)
    type = models.CharField(max_length=10, blank=True, null=False)
    size = models.CharField(max_length=13, blank=True, null=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Chunk(models.Model):
    uploaded_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name="file_chunks"
    )
    chunk_file = CloudinaryField(
        folder=get_folder_path("file_chunks"),
        resource_type='auto'
    )
    # The position of the chunk file when splitted
    # e.g chunk (1), chunk (2), chunk (3), ...
    position = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.uploaded_file} chunk"
