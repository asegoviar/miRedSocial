from django.urls import path
from .api_views import (
    MyConversationsAPIView,
    StartConversationAPIView,
    ConversationMessagesAPIView,
    SendMessageAPIView
)

app_name = "chat_api"

urlpatterns = [

    # Obtener todas mis conversaciones
    path("conversations/", MyConversationsAPIView.as_view(), name="my_conversations"),

    # Iniciar conversación (o devolverla si ya existe)
    path("start/<int:user_id>/", StartConversationAPIView.as_view(), name="start_conversation"),

    # Obtener mensajes de una conversación
    path("<int:convo_id>/messages/", ConversationMessagesAPIView.as_view(), name="conversation_messages"),

    # Enviar mensaje
    path("<int:convo_id>/send/", SendMessageAPIView.as_view(), name="send_message"),
]
