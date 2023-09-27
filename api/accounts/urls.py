from django.urls import path
from . import views

urlpatterns = [
    path('auth/users/', views.UserListView.as_view(), name='users-list')
]