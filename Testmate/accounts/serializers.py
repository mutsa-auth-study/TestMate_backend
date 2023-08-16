from .models import User
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'kakao_id', 'profile_nickname', 'profile_image', 'email')