import uuid

from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.auth import get_user_model
from django.db import models


class File(models.Model):
    """
    A model to represent files uploaded by users.

    This model stores information about uploaded files, including the user who uploaded them,
    the name of the file, and the file itself. It uses RawMediaCloudinaryStorage to handle
    file uploads, making it possible to upload various types of files.
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
    name = models.CharField(max_length=255, blank=True, null=False)

    # The choice of ImageField for 'file' is random because RawMediaCloudinaryStorage 
    # allows uploading various file types, not just images.
    file = models.ImageField(
        upload_to='raw/',
        storage=RawMediaCloudinaryStorage()
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
