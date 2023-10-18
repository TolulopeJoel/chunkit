import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models

from .utils import get_folder_path


class UploadedFile(models.Model):
    """
    A model to represent files uploaded by users.
    This model stores information about uploaded files, including the user who uploaded them,
    the name of the file, and the file itself.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='uploaded_files'
    )
    url = CloudinaryField(
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
    """
    Represents a chunk of an uploaded file.

    This model stores information about each chunk of an uploaded file, including its position within the file,
    a reference to the original uploaded file, and the URL where the chunk is stored in Cloudinary.
    """

    position = models.PositiveIntegerField()
    uploaded_file = models.ForeignKey(
        UploadedFile,
        on_delete=models.CASCADE,
        related_name="file_chunks"
    )
    chunk_url = CloudinaryField(
        folder=get_folder_path("file_chunks"),
        resource_type='auto'
    )

    def __str__(self):
        return f"{self.uploaded_file} chunk"
