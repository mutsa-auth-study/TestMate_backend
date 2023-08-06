# from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import viewsets



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
        post = get_object_or_404(Post, pid=pid) #id는 변수로 선언되지 않음, pid=pid로 수정
        serializer = PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

#여기서부터는 mixins을 사용한 view작성입니다. 위의 코드와 같은 기능을 구현합니다.
#단지, 사용자친화적인 폼을 볼 수 있기에 시도해보고 있습니다.

from rest_framework import generics
from rest_framework import mixins
class PostsAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request,*args, **kwargs):
        return self.create(request,*args, **kwargs)

class PostAPIMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Post.objects.all() 
    serializer_class = PostSerializer #이게 맞나..모르겠음
    lookup_field = 'pid'

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
#아직 수정하기와 삭제하기 기능은 없음 -> 책 123p에 나와있음, 참고!