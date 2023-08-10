from rest_framework import serializers

from .models import LocationComment, LocationInfo

class LocationCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationComment
        fields = '__all__'

class LocationInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationInfo
        fields = '__all__'