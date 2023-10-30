from django.contrib import admin

from .models import Chunk, UploadedFile

class FileAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'uploaded_at']

admin.site.register(UploadedFile, FileAdmin)
admin.site.register(Chunk)
