from django.urls import path

from . import views

urlpatterns = [
    path('chunks/<int:file_id>/', views.ChunkListView.as_view(), name='chunks-list'),
    path('chunks/', views.ChunkCreateView.as_view(), name='chunks-create'),
    path('uploaded-files/', views.UploadedFileListCreateView.as_view(), name='files-list-create'),
]
