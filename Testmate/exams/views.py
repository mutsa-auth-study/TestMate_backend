from rest_framework import generics
from rest_framework import mixins

from .models import Exam, ExamPlan
from .serializers import ExamTotalSerializer, ExamDetailSerializer

class ExamTotalAPIMixins(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamTotalSerializer
    # GET 메소드 처리 (전체목록)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class ExamDetailAPIMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = ExamPlan.objects.all()
    serializer_class = ExamDetailSerializer
    lookup_field = 'exam_id'
    
    # GET 메소드 처리 (시험ID에 해당하는 1개의 시험 일정 불러옴)
    def get(self, request,*args, **kwargs):
        return self.retrieve(request, *args, **kwargs)