from django.urls import path
# from .views import ExamDetailAPIMixins, ExamTotalAPIMixins

from .views import ExamDetail
#from .views import setExamDB_XML, deleteExamDB_XML

urlpatterns = [
    #path("", ExamTotalAPIMixins.as_view()),
    # path("<int:exam_id>/", ExamDetailAPIMixins.as_view()),
    path("<int:exam_id>/", ExamDetail.as_view(), name='getExamPlan'),

    # path("setDB/", setExamDB.as_view(), name='setDB'),
    # path("setDBXML/", setExamDB_XML.as_view(), name='setDBXML'),
    # path("delDBXML/", deleteExamDB_XML.as_view(), name='delDBXML'),
]
