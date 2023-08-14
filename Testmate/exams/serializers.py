from rest_framework import serializers

from .models import Exam, ExamPlan, ExamRecent

class ExamTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ("exam_id","qualgbcd","qualgbnm", "seriescd","seriesnm","jmcd","jmfldnm", "obligfldcd", "obligfldnm", "mdobligfldcd", "mdobligfldnm", "is_favorite")  


class ExamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamPlan
        fields = ("exam_plan_id","exam_id","implYy","implSeq","description", "docRegStartDt", "docRegEndDt", "docExamStartDt", "docExamEndDt", "docPassDt", "pracRegStartDt", "pracRegEndDt", "pracExamStartDt", "pracExamEndDt", "pracPassDt")

class ExamRecentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamRecent
        fields = '__all__'