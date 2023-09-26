import uuid

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.db import models


class File(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='files'
    )

    name = models.CharField(max_length=255)
    file = CloudinaryField('file')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
