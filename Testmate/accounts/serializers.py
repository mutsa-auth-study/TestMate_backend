from .models import User
from rest_framework import serializers


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'profile_nickname', 'email', 'profile_image')