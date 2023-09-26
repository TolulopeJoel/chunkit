from django.urls import path

from . import views

urlpatterns = [
    path('file/', views.FileListCreateView.as_view(), name='file-list-create'),
]
