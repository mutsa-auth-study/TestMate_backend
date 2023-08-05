from .views import PostAPI, PostsAPI
from django.urls import path

urlpatterns = [
    path("posts/", PostsAPI.as_view()),
    path("post/<int:pid>/", PostAPI.as_view()),
]