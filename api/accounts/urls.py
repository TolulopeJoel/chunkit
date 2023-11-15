from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CustomTokenObtainPairView

from . import views

urlpatterns = [
    path('users/', views.UserListView.as_view(), name='users-list'),

    # Endpoint to obtain a JWT token
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Endpoint to refresh an expired JWT token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Endpoint to verify the validity of a JWT token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
