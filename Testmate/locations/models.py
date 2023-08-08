from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
class LocationComment(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE,null=False) # ForeignKey이므로 null=False 필수
    # 카카오 로그인 구현 후, reviewer 가져올 로직 생각해봐야 함 
    content = models.TextField('내용')
    created_at = models.DateTimeField('작성일', default=timezone.now)
    noise = models.IntegerField('소음', default=0, blank=True)
    cleanness = models.IntegerField('청결도', default=0, blank=True)
    accessibility = models.IntegerField('접근성', default=0, blank=True)
    facility = models.IntegerField('시설 및 장비', default=0, blank=True)
    average = models.FloatField('평균', default=0.0, blank=True)

    def save(self, *args, **kwargs):
        # Calculate the average value
        total = self.noise + self.cleanness + self.accessibility + self.facility
        num = 4  # Assuming you have 4 rating fields, adjust if you have more or less.
        self.average = total / num
        super(LocationComment, self).save(*args, **kwargs)

    
class LocationInfo(models.Model):
    location_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 하단의 항목들은 information이라는 리스트로 다 들어가 있음
    address = models.CharField(max_length=100) # 시험장소 주소
    brchCd = models.IntegerField() # 지사코드
    brchNm = models.CharField(max_length=100) # 지사명
    examAreaGbNm = models.CharField(max_length=100) # 시행장소 구분
    examAreaNm = models.CharField(max_length=100) # 시행장소명
    plceLoctGid = models.CharField(max_length=500) # 장소위치안내
    telNo = models.CharField(max_length=50) # 전화번호
    latitude = models.FloatField() # 위도
    longtitude = models.FloatField() # 경도