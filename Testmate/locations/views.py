# from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets

from rest_framework import generics
from rest_framework import mixins

from .models import Post
from .serializers import PostSerializer, PostCreateSerializer
from .permissions import CustomReadOnly

class PostsAPI(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    def post (self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostAPI(APIView):
    def get(self, request, pid):
        post = get_object_or_404(Post, pid=id)
        serializer = PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)