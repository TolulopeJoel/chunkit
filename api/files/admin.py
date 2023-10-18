from django.contrib import admin

from .models import UploadedFile

class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'uploaded_at']

admin.site.register(UploadedFile, FileAdmin)
