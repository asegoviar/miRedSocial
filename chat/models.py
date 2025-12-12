from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    """
    Una conversación entre 2 usuarios.
    Si quisieras chats grupales después, este modelo se multiplica.
    """
    user1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations_user1"
    )
    user2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="conversations_user2"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Evita conversaciones duplicadas

    def __str__(self):
        return f"Conversación entre {self.user1.username} y {self.user2.username}"


class Message(models.Model):
    """
    Mensajes dentro de una conversación.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Para ordenar automáticamente por fecha
    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Mensaje de {self.sender.username} en conv {self.conversation.id}"
