from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk","content","created_at", "noise","cleanness","accessibility","facility")  # pk는 Post model의 기본키
    #미완성


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("content","noise","cleanness","accessibility","facility")