from django.urls import path
from .views import ExamDetailAPIMixins, ExamTotalAPIMixins

urlpatterns = [
    path("", ExamTotalAPIMixins.as_view()),
    path("<int:exam_id>/", ExamDetailAPIMixins.as_view()),
]
