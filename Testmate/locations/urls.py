from .views import PostsAPIMixins, PostAPIMixins
from django.urls import path

urlpatterns = [
    path("comment/",PostsAPIMixins.as_view()),
    path("comment/<int:pid>/",PostAPIMixins.as_view()),
]