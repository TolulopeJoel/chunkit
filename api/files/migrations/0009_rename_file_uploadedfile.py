# Generated by Django 4.2.5 on 2023-10-18 22:44

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0008_rename_file_file_url_file_size_file_type_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='File',
            new_name='UploadedFile',
        ),
    ]
