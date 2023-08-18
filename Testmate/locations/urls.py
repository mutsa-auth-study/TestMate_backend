from django.urls import path
from .views import *

urlpatterns = [
    path("", NearestLocation.as_view(), name='NearestLocationList'), # 고사장 확인 [GET]
    path("comment/<uuid:location_id>/", getLocationComment.as_view(), name="LocationCommentList"), # 고사장 리뷰 조회 [GET]
    path("comment/", LocationCommentView.as_view(), name='LocationComment'), # 고사장 리뷰 [POST, PATCH, DELETE]
    path("mycomment/", Mycomment.as_view(), name='MyLocationCommentList'), # 작성 고사장 리뷰 조회[GET]
    
    # path("setDB/", setLocationDB.as_view(), name='setLocationDB'),
    # path("delDB/", deleteLocationDB.as_view(), name='delLocationDB'),
]