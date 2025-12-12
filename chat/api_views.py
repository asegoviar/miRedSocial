from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.contrib.auth.models import User
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    CreateMessageSerializer
)


class MyConversationsAPIView(APIView):
    """
    Lista todas mis conversaciones existentes.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        conversations = (
            Conversation.objects.filter(user1=user) |
            Conversation.objects.filter(user2=user)
        ).order_by("-created_at")

        serializer = ConversationSerializer(
            conversations, many=True, context={"request": request}
        )

        return Response(serializer.data, status=200)


class StartConversationAPIView(APIView):
    """
    Crea una conversación con otro usuario si no existe.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        me = request.user

        if me.id == user_id:
            return Response(
                {"error": "No puedes chatear contigo mismo."},
                status=400
            )

        try:
            other = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado."},
                status=404
            )

        # Verificar si ya existe una conversación (me, other) o (other, me)
        convo = Conversation.objects.filter(
            user1=me, user2=other
        ).first() or Conversation.objects.filter(
            user1=other, user2=me
        ).first()

        if convo:
            serializer = ConversationSerializer(
                convo, context={"request": request}
            )
            return Response(serializer.data, status=200)

        # Crear nueva conversación
        convo = Conversation.objects.create(user1=me, user2=other)

        serializer = ConversationSerializer(
            convo, context={"request": request}
        )
        return Response(serializer.data, status=201)


class ConversationMessagesAPIView(APIView):
    """
    Devuelve todos los mensajes ordenados de una conversación.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, convo_id):
        try:
            convo = Conversation.objects.get(id=convo_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversación no encontrada."},
                status=404
            )

        # Evitar leer conversaciones ajenas
        if request.user not in [convo.user1, convo.user2]:
            return Response(
                {"error": "No tienes permiso."},
                status=403
            )

        messages = convo.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=200)


class SendMessageAPIView(APIView):
    """
    Envía un mensaje a una conversación existente.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, convo_id):
        try:
            convo = Conversation.objects.get(id=convo_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversación no encontrada."},
                status=404
            )

        # Seguridad
        if request.user not in [convo.user1, convo.user2]:
            return Response(
                {"error": "No tienes permiso."},
                status=403
            )

        serializer = CreateMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        message = Message.objects.create(
            conversation=convo,
            sender=request.user,
            content=serializer.validated_data["content"]
        )

        return Response(
            MessageSerializer(message).data,
            status=201
        )
