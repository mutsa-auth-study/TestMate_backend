from django.urls import path

from .views import ExamList, ExamDetail, RecentExamListView
#from .views import setExamDB_XML, deleteExamDB_XML

urlpatterns = [
    path("", ExamList.as_view(), name='getExamList'),
    path("<str:exam_id>/", ExamDetail.as_view(), name='getExamDetail'),
    path("recent/", RecentExamListView.as_view(), name='getRecentExam'),

    # path("setDB/", setExamDB.as_view(), name='setDB'),
    # path("setDBXML/", setExamDB_XML.as_view(), name='setDBXML'),
    # path("delDBXML/", deleteExamDB_XML.as_view(), name='delDBXML'),
]