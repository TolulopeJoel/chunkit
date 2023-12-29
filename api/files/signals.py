import cloudinary
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import UploadedFile


@receiver(pre_delete, sender=UploadedFile)
def uploaded_file_delete(sender, instance, **kwargs):
    """
    Signal handler to delete the file associated with an uploadedfile before it is deleted.
    This uses the Cloudinary API to delete the image from the Cloudinary storage.
    """
    cloudinary.uploader.destroy(instance.file.public_id)
