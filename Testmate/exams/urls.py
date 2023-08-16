from django.urls import path
from .views import *

urlpatterns = [
    path("", ExamListView.as_view(), name='ExamList'),
    path("<str:exam_id>/", ExamDetailView.as_view(), name='ExamDetail'),
    path("favorite/", ExamFavoriteView.as_view(), name='ExamFavorite'),
    path("recent/", ExamRecentView.as_view(), name='ExamRecent'),

    # path("setDB/", setExamDB.as_view(), name='setDB'),
    # path("setDBXML/", setExamDB_XML.as_view(), name='setDBXML'),
    # path("delDBXML/", deleteExamDB_XML.as_view(), name='delDBXML'),
]