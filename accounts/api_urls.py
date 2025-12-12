# accounts/api_urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .api_views import *

app_name = "accounts_api"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    # Login (obtener access + refresh)
    path("login/", TokenObtainPairView.as_view(), name="login"),

    # Refresh (obtener nuevo access desde refresh)
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),

    # Usuario autenticado (perfil)
    path("me/", MeAPIView.as_view(), name="me"),

    # 🔥 Endpoint que te faltaba:
    path("profile/update/", UpdateProfileView.as_view(), name="profile_update"),
    path("users/", UserListAPIView.as_view(), name="user_list"),
]
