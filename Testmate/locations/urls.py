from .views import createLocationComment, getLocationComment
from django.urls import path

urlpatterns = [
    path("comment/",createLocationComment.as_view()),
    path("comment/<uuid:location_id>/",getLocationComment.as_view()),
]