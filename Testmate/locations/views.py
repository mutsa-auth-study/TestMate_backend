from rest_framework import generics
#from rest_framework import mixins

from .models import LocationComment, LocationInfo #모델
from .serializers import LocationCommentSerializer, LocationInfoSerializer #시리얼라이저

from rest_framework.views import Response, status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import response, status
import xml.etree.ElementTree as ET
import requests
from rest_framework.generics import get_object_or_404


# 고사장 리뷰 작성 [POST][/location/comment]
class createLocationComment(APIView):
    def post(self, request,*args, **kwargs):
        serializer = LocationCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 고사장 리뷰 조회 [GET][/location/comment/<uuid:location_id>] #location_id는 고사장 id
class getLocationComment(APIView):
    def get(self, request, *args, **kwargs):
        location_id = kwargs.get('location_id')
        locationComment = LocationComment.objects.filter(location_id=location_id)

        # location_id와 일치하는 데이터가 없을 경우 404 응답을 반환
        if not locationComment.exists():
            return Response({"detail": "Location comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 페이지네이션 적용
        paginator = PageNumberPagination()
        paginated_comments = paginator.paginate_queryset(locationComment,request)
        serializer = LocationCommentSerializer(paginated_comments, many=True)

        return paginator.get_paginated_response(serializer.data)


# 고사장 리뷰 수정 [PATCH][/location/comment/<uuid:location_id>] #location_id는 고사장 id

# 고사장 리뷰 삭제 [DELETE][/location/comment/<uuid:location_id>] #location_id는 고사장 id

# 수정, 삭제도 location_id 필요하지 않을까?

# 고사장 확인 [GET][/location]
#for location in (우리 DB에 있는 고사장들)
	# location.addr 추출
	# 위도, 경도와 함께 지도 API 호출
	# 최단거리 리스트 10개 이내에 속하면 갱신
# 최단거리 10개 반환


# 고사장 정보 DB에 넣기
class setLocationDB(APIView):
    decodedKey = "" # 발급받아야함
    endPoint = "요청url" # 요청url 없음

    def get(self, request, *args, **kwargs):
        def callAPI(brchCd):
            # latitude = request_data['latitude'] #request
            # longtitude = request_data['longtitude'] #request
            # 위경도 request는 공공데이터 api 호출할때는 필요없는데..어떻게 처리?

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
        
        LocationInfo = callAPI(request_data["brchCd"])
        LocationInfo["location_id"] = request_data["location_id"]

        serializer = LocationInfoSerializer(data=LocationInfo)
        
        if serializer.is_valid():
            serializer.save() #데이터베이스에 저장
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)