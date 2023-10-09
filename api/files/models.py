import uuid
from datetime import datetime

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models


def get_folder_path():
    """
    Generate a folder path for cloudinary file based
    on the current date and week number.
    """

    # Current date and time
    now = datetime.now()

    # Calculate the week number of current month
    day_of_month = datetime.now().day
    week_number = (day_of_month - 1) // 7 + 1

    folder_path = f'media/files/{now.year}/{now.month}/{week_number}'

    return folder_path


class File(models.Model):
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
    name = models.CharField(max_length=255, blank=True, null=False)
    file = CloudinaryField(
        folder=get_folder_path(),
        resource_type='auto'
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
