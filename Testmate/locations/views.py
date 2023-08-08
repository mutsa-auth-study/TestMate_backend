from rest_framework import generics
from rest_framework import mixins

from .models import LocationComment
from .serializers import PostSerializer, PostCreateSerializer

class PostsAPIMixins(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = LocationComment.objects.all()
    serializer_class = PostSerializer
    # GET 메소드 처리 (전체목록)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    # POST 메소드 처리 (1개 등록)
    def post(self, request,*args, **kwargs):
        return self.create(request,*args, **kwargs)

class PostAPIMixins(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = LocationComment.objects.all() 
    serializer_class = PostSerializer #이게 맞나..모르겠음
    lookup_field = 'pid'
    # GET 메소드 처리 (1개 등록)
    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)
    
    # PUT 메소드 처리 (1개 수정)
    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    # DELETE 메소드 처리 (1개 삭제)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args, **kwargs)
