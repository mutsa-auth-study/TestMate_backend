
from .views import PostAPI, PostsAPI ,PostsAPIMixins, PostAPIMixins
from django.urls import path

urlpatterns = [
    path("posts/", PostsAPI.as_view()),
    path("post/<uuid:pid>/", PostAPI.as_view()), #Post모델에서 pid를 UUIDField로 정의하고 있음
    path("mixin/posts/",PostsAPIMixins.as_view()),
    path("mixin/post/<uuid:pid>/",PostAPIMixins.as_view()),
]