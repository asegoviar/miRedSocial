# accounts/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import status
from .models import Profile


class MeAPIView(APIView):
    """
    GET /api/auth/me/
    Devuelve los datos del usuario autenticado vía JWT.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)
    

class RegisterAPIView(APIView):
    """
    POST /api/auth/register/
    Registro moderno usando DRF.
    """
    permission_classes = [AllowAny]  # cualquiera puede registrarse

    def post(self, request):
        username = request.data.get("username", "").strip()
        email = request.data.get("email", "").strip()
        password = request.data.get("password", "")
        password2 = request.data.get("password2", "")

        # --- Validaciones necesarias ---
        if not username or not email or not password or not password2:
            return Response(
                {"error": "Todos los campos son obligatorios."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if password != password2:
            return Response(
                {"error": "Las contraseñas no coinciden."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(password) < 8:
            return Response(
                {"error": "La contraseña debe tener al menos 8 caracteres."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "El nombre de usuario ya está en uso."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "El email ya está registrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # --- Crear usuario ---
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Crear perfil automáticamente
        Profile.objects.create(user=user)

        # Serializar para devolver algo útil
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        profile = user.profile

        # Datos del usuario (User)
        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)

        # Datos del profile (Profile)
        profile.bio = request.data.get("bio", profile.bio)
        profile.birthdate = request.data.get("birthdate", profile.birthdate)
        
        is_private_raw = request.data.get("is_private", profile.is_private)
        if str(is_private_raw).lower() == "true":
            profile.is_private = True
        elif str(is_private_raw).lower() == "false":
            profile.is_private = False


        avatar = request.FILES.get("avatar")
        if avatar:
            profile.avatar = avatar

        user.save()
        profile.save()

        return Response({"updated": True}, status=200)
    

class UserListAPIView(APIView):
    """
    Lista todos los usuarios (excepto yo).
    Sirve para iniciar una conversación desde el chat.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.exclude(id=request.user.id)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

