from .views import PostsAPIMixins, PostAPIMixins
from django.urls import path

urlpatterns = [
    path("",PostsAPIMixins.as_view()),
    path("<int:pid>/",PostAPIMixins.as_view()),
]