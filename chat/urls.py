from django.urls import path
from django.shortcuts import render

def chat_page(request):
    return render(request, "chat/chat.html")

urlpatterns = [
    path("", chat_page, name="chat_page"),
]
