from django.urls import path
# from .views import ExamDetailAPIMixins, ExamTotalAPIMixins

from .views import ExamList, ExamPlan
#from .views import setExamDB_XML, deleteExamDB_XML

urlpatterns = [
    path("", ExamList.as_view(), name='getExamList'),
    path("<int:exam_id>/", ExamPlan.as_view(), name='getExamDetail'),

    # path("setDB/", setExamDB.as_view(), name='setDB'),
    # path("setDBXML/", setExamDB_XML.as_view(), name='setDBXML'),
    # path("delDBXML/", deleteExamDB_XML.as_view(), name='delDBXML'),
]
