from django.db import models
import uuid
#import 
# Create your models here.

class Exam(models.Model):
    exam_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    qualgbcd = models.CharField(max_length=100) # 자격구분
    qualgbnm = models.CharField(max_length=100) # 자격구분명
    seriescd = models.CharField(max_length=100) #계열코드
    seriesnm = models.CharField(max_length=100) # 계열명
    jmcd = models.CharField(max_length=100) # 종목코드
    jmfldnm = models.CharField(max_length=100) # 종목명
    obligfldcd = models.CharField(max_length=100, blank=True) # 대직무분야코드
    obligfldnm = models.CharField(max_length=100, blank=True) # 대직무분야명
    mdobligfldcd = models.CharField(max_length=100, blank=True) # 중직무분야코드
    mdobligfldnm = models.CharField(max_length=100, blank=True) # 중직무분야명
    # 국가전문자격의 경우 분야가 없어 빈칸 허용
    # is_favorite 삭제

class ExamPlan(models.Model):
    exam_plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    exam_id = models.ForeignKey(Exam,on_delete=models.CASCADE,blank=False) # 위에 있는 Exam모델의 기본키를 외래키로
    implYy = models.CharField(max_length=100) # 시행년도
    implSeq = models.CharField(max_length=100) # 시행회차
    description = models.CharField(max_length=100) # 설명
    docRegStartDt = models.CharField(max_length=100, blank=True) # 필기시험 원서접수 시작일자
    docRegEndDt = models.CharField(max_length=100, blank=True) # 필기시험 원서접수 종료일자
    docExamStartDt = models.CharField(max_length=100, blank=True) # 필기시험 시작일자
    docExamEndDt = models.CharField(max_length=100, blank=True) # 필기시험 종료일자
    docPassDt = models.CharField(max_length=100, blank=True) # 필기시험 합격(예정)자 발표일자
    pracRegStartDt = models.CharField(max_length=100, blank=True) # 실기(작업)/면접 시험 원서접수 시작일자
    pracRegEndDt = models.CharField(max_length=100, blank=True) # 실기(작업)/면접 시험 원서접수 종료일자
    pracExamStartDt = models.CharField(max_length=100, blank=True) # 실기(작업)/면접 시험 시작일자
    pracExamEndDt = models.CharField(max_length=100, blank=True) # 실기(작업)/면접 시험 종료일자
    pracPassDt = models.CharField(max_length=100, blank=True) # 실기(작업)/면접 합격자 발표일자

class ExamFavorite(models.Model):
    favorite_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False) # Exam class의 기본키 참조
    #user_id = 로그인된 사용자라 accounts의 모델이 만들어져야 외래키로 가져올 수 있을 듯..
    #user_id 살려야함!!


class ExamRecent(models.Model):
    recent_id = models.AutoField(primary_key=True)
    # UUID는 명확한 시간 순서 보장X -> AutoField로 변경 : 자동 증가 정수
    exam_id = models.ForeignKey(Exam, on_delete=models.CASCADE, blank=False) # Exam class의 기본키 참조
    # user_id = 로그인된 사용자라 accounts의 모델이 만들어져야 외래키로 가져올 수 있을 듯..

    # def save(self, *args, **kwargs):
    #     if not self.custom_id:
    #         # id 필드가 없을 경우, 가장 큰 id 값에 1을 더한 값을 사용
    #         last_id = ExamRecent.objects.aggregate(models.Max('recent_id'))['recent_id__max']
    #         self.custom_id = last_id + 1 if last_id is not None else 1
    #     super(ExamRecent, self).save(*args, **kwargs)