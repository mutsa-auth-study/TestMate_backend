from django.urls import path
from .views import ExamDetailAPIMixins, ExamTotalAPIMixins

from .views import ExamDetail

urlpatterns = [
    path("", ExamTotalAPIMixins.as_view()),
    # path("<int:exam_id>/", ExamDetailAPIMixins.as_view()),
    path("<int:exam_id>/", ExamDetail.as_view(), name='getExamPlan'),
]
