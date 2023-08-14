from .views import createLocationComment, getLocationComment, updateLocationComment,deleteLocationComment, MainLocationCommentView
from django.urls import path

urlpatterns = [
    #path("comment/",createLocationComment.as_view()),
    path("comment/<uuid:location_id>/",getLocationComment.as_view()),

    #path('location/comment/', MainLocationCommentView.as_view()),
    path('location/comment/', MainLocationCommentView.as_view(), name='location-comment'),
    path('location/comment/<uuid:user_id>/<uuid:location_id>/', MainLocationCommentView.as_view(), name='location-comment-specific'),
]