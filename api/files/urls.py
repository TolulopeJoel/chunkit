from django.urls import path

from . import views

urlpatterns = [
    path(
        'uploaded-files/', views.UploadedFileListCreateView.as_view(), name='uploaded-files-list-create'
    ),
]
