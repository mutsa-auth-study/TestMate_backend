from django.db import models
import uuid
# Create your models here.

class Exam(models.Model):
    exam_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualgbcd = models.CharField(max_length=100) # 자격구분
    qualgbnm = models.CharField(max_length=100) # 자격구분명
    seriescd = models.CharField(max_length=100) #계열코드
    seriesnm = models.CharField(max_length=100) # 계열명
    jmcd = models.CharField(max_length=100) # 종목코드
    jmfldnm = models.CharField(max_length=100) # 종목명
    obligfldcd = models.CharField(max_length=100) # 대직무분야코드
    obligfldnm = models.CharField(max_length=100) # 대직무분야명
    mdobligfldcd = models.CharField(max_length=100) # 중직무분야코드
    mdobligfldnm = models.CharField(max_length=100) # 중직무분야명
    # 대직무분야코드/ 중직무분야코드 erd에는 있고 api 명세서에 없어서 일단 추가함
    is_favorite = models.BooleanField(default=False)
    # default = False로 해둠 => 일단은 즐찾이 없는 상태로 시작

class ExamPlan(models.Model):
    exam_plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_id = models.ForeignKey(Exam,on_delete=models.CASCADE,null=False) # 위에 있는 Exam모델의 기본키를 외래키로
    implYy = models.CharField(max_length=100) # 시행년도
    implSeq = models.CharField(max_length=100) # 시행회차
    description = models.CharField(max_length=100) # 설명
    docRegStartDt = models.CharField(max_length=100) # 필기시험 원서접수 시작일자
    docRegEndDt = models.CharField(max_length=100) # 필기시험 원서접수 종료일자
    docExamStartDt = models.CharField(max_length=100) # 필기시험 시작일자
    docExamEndDt = models.CharField(max_length=100) # 필기시험 종료일자
    docPassDt = models.CharField(max_length=100) # 필기시험 합격(예정)자 발표일자
    pracRegStartDt = models.CharField(max_length=100) # 실기(작업)/면접 시험 원서접수 시작일자
    pracRegEndDt = models.CharField(max_length=100) # 실기(작업)/면접 시험 원서접수 종료일자
    pracExamStartDt = models.CharField(max_length=100) # 실기(작업)/면접 시험 시작일자
    pracExamEndDt = models.CharField(max_length=100) # 실기(작업)/면접 시험 종료일자
    pracPassDt = models.CharField(max_length=100) # 실기(작업)/면접 합격자 발표일자