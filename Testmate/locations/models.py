from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
User = get_user_model()
# Create your models here.
class LocationComment(models.Model):
    location_comment_id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE,null=False) # ForeignKey이므로 null=False 필수
    # 카카오 로그인 구현 후, user_id(reviewer) 가져올 로직 생각해봐야 함
    #location_id = models.ForeignKey('LocationInfo', on_delete=models.CASCADE,null=False) # ForeignKey이므로 null=False 필수
    location_id = models.ForeignKey('LocationInfo', on_delete=models.CASCADE, null=True)
    # migration이 안되서 일단 -> location_id 필드를 nullable로 설정함
    # 이렇게 하면 기존의 행들은 null 값을 가질 것이고, 나중에 필요한 값을 설정할 수 있음
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
    brchNm = models.CharField(max_length=100) # 지사명
    examAreaGbNm = models.CharField(max_length=100, blank=True) # 시행장소 구분
    examAreaNm = models.CharField(max_length=100) # 시행장소명
    plceLoctGid = models.CharField(max_length=100, default="", blank=True) # 장소위치안내
    telNo = models.CharField(max_length=100, default="", blank=True) # 전화번호
    latitude = models.FloatField(max_length=100, default=0.0) # 위도
    longitude = models.FloatField(max_length=100, default=0.0) # 경도
