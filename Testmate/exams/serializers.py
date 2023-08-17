from rest_framework import serializers

from .models import Exam, ExamPlan, ExamRecent

class ExamTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamPlan
        fields = '__all__'

class ExamRecentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRecent
        fields = '__all__'