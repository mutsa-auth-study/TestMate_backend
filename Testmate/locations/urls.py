from .views import getLocationComment, MainLocationCommentView
from django.urls import path

urlpatterns = [
    path("comment/<uuid:location_id>/", getLocationComment.as_view()), # 고사장 리뷰 조회 [GET]
    path('comment/', MainLocationCommentView.as_view(), name='location-comment'), # 고사장 리뷰[POST, PATCH, DELETE]
]