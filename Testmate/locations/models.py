from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

# Create your models here.
class Post(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
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
        super(Post, self).save(*args, **kwargs)