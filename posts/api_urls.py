from django.urls import path
from .api_views import *
app_name = "posts_api"

urlpatterns = [
    # Crear un post nuevo
    path("create/", CreatePostAPIView.as_view(), name="create_post"),

    # Feed de posts
    path("feed/", FeedPostsAPIView.as_view(), name="feed_posts"),

    # Crear comentario sobre un post
    path("<int:post_id>/comments/create/", CreateCommentAPIView.as_view(), name="create_comment"),

    # Obtener comentarios de un post
    path("<int:post_id>/comments/", PostCommentsAPIView.as_view(), name="post_comments"),
    path("my/", MyPostsAPIView.as_view(), name="my_posts"),

]
