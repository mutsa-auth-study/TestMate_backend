from .views import PostAPI, PostsAPI ,PostsAPIMixins, PostAPIMixins
from django.urls import path

urlpatterns = [
    path("", PostsAPI.as_view()),
    path("<uuid:pid>/", PostAPI.as_view()), #Post모델에서 pid를 UUIDField로 정의하고 있기 때문에 int -> uuid 수정함
    path("mixin/",PostsAPIMixins.as_view()),
    path("mixin/<uuid:pid>/",PostAPIMixins.as_view()),
]