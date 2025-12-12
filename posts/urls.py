from django.urls import path
from .views import feed_page

urlpatterns = [
    path("feed/", feed_page, name="feed_page"),
]
