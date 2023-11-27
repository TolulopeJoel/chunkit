from django.urls import path

from . import views

urlpatterns = [
    path('chunks/', views.ChunkCreateView.as_view(), name='chunks-create'),
    path('files/', views.UploadedFileListCreateView.as_view(), name='files-list-create'),
]
