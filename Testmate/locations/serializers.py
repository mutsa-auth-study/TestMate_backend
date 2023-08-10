from rest_framework import serializers

from .models import LocationComment, LocationInfo

class LocationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationComment
        fields = ("pid","content","created_at", "noise","cleanness","accessibility","facility")

'''
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationComment
        fields = ("content","noise","cleanness","accessibility","facility")
'''
# PostCreateSerializer를 참조한 뷰가 없어서 일단 주석처리

class LocationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInfo
        fields = '__all__'