from django.urls import path

from . import views

urlpatterns = [
    path('chunks/', views.ChunkListCreateView.as_view(), name='chunks-list-create'),
    path(
        'uploaded-files/', views.UploadedFileListCreateView.as_view(), name='uploaded-files-list-create'
    ),
]
