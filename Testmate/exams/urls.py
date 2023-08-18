from django.urls import path
from .views import *

urlpatterns = [
    path("main/", ExamMainView.as_view(), name='ExamMain'), # 메인페이지 [GET]
    path("", ExamListView.as_view(), name='ExamList'), # 시험 목록 조회 [GET]
    path("detail/<str:exam_id>/", ExamDetailView.as_view(), name='ExamDetail'), # 시험 상세 조회 [POST]
    path("favorite/", ExamFavoriteView.as_view(), name='ExamFavorite'), # 즐겨찾기 시험 조회 [GET, POST, DELETE]
    path("recent/", ExamRecentView.as_view(), name='ExamRecent'), # 최근조회 시험 조회 [GET]


    # path("setDB/", setExamDB.as_view(), name='setDB'),
    # path("setDBXML/", setExamDB_XML.as_view(), name='setDBXML'),
    # path("delDBXML/", deleteExamDB_XML.as_view(), name='delDBXML'),
]