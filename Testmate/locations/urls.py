from django.urls import path
from .views import *

urlpatterns = [
    path("", NearestLocation.as_view(), name='NearestLocationList'),
    path("comment/<uuid:location_id>/", getLocationComment.as_view(), name="LocationCommentList"), # 고사장 리뷰 조회 [GET]
    path('comment/', MainLocationCommentView.as_view(), name='locationComment'), # 고사장 리뷰[POST, PATCH, DELETE]

    path("setDB/", setLocationDB.as_view(), name='setLocationDB'),
]