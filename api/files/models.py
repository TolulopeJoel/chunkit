from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField


class UserFile(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='products'
    )

    name = models.CharField(max_length=255)
    file = CloudinaryField('file')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.name
