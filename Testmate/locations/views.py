from rest_framework import generics
#from rest_framework import mixins

from .models import LocationComment, LocationInfo
from .serializers import LocationCommentSerializer, LocationInfoSerializer

from rest_framework.views import APIView
from rest_framework import response, status
import xml.etree.ElementTree as ET
import requests

'''
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
'''
#고사장 확인 [GET][/location]
class InfoDetail(APIView):
    decodedKey = "" #발급받아야함
    endPoint = "요청url" #요청url 없음

    def get(self, request, *args, **kwargs):
        def callAPI(latitude, longtitude):
            latitude = request_data['latitude'] #request
            longtitude = request_data['longtitude'] #request
            #위경도 request는 공공데이터 api 호출할때는 필요없는데..어떻게 처리?
            params = {"serviceKey": self.decodedKey,
            "brchCd": "서울",
            "numOfRows": 10,
            "pageNo": 1
            }
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            dict = {}
            for item in root.findall('.//item'):
                dict["address"] = item.find('address').text
                dict["brchCd"] = item.find('brchCd').text
                dict["brchNm"] = item.find('brchNm').text
                dict["examAreaGbNm"] = item.find('examAreaGbNm').text
                dict["examAreaNm"] = item.find('examAreaNm').text
                dict["plceLoctGid"] = item.find('placeLoctGid').text
                dict["telNo"] = item.find('telNo').text
                
            return dict
        
        request_data = request.data
        # additional_info = request.META.get('HTTP_X_ADDITIONAL_INFO', None)  # 예시로 요청 헤더에서 추가 정보를 가져옴
        # 이해안감
        LocationInfo = "" # 위경도값은 api에서 가져오지 않음
        LocationInfo["location_id"] = request_data["location_id"]

        serializer = LocationInfoSerializer(data=LocationInfo)
        
        if serializer.is_valid():
            serializer.save() #데이터베이스에 저장
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)