from django.urls import path
from .views import ExamDetailAPIMixins, ExamTotalAPIMixins

urlpatterns = [
    path("exam/", ExamTotalAPIMixins.as_view()),
    path("exam/<int:exam_id/", ExamDetailAPIMixins.as_view()),
]
