from django.urls import path

from .views import ExamDetail,RecentExamListView

urlpatterns = [
    path("<int:exam_id>/", ExamDetail.as_view(), name='getExamPlan'),
    path("recent/", RecentExamListView.as_view(), name='getRecentExam'),
]
