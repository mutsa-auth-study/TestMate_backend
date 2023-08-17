from rest_framework import generics
#from rest_framework import mixins
#from rest_framework import viewsets
from uuid import UUID
from django.views import View

from .models import LocationComment, LocationInfo # 모델
from .serializers import LocationCommentSerializer, LocationInfoSerializer # 시리얼라이저
#from .permissions import CustomReadOnly # 권한 -> 근데 이거 안쓰고 drf에서 제공하는 permissions 쓰면 될듯
from rest_framework import permissions # 로그인 권한
import json
from django.http import JsonResponse

from rest_framework.views import Response, status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .pagination import CustomPageNumberPagination
from rest_framework import response, status
import xml.etree.ElementTree as ET
import requests
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny

# 고사장 리뷰 조회 [GET][/location/comment/<uuid:location_id>] #location_id는 고사장 id
class getLocationComment(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        location_id = kwargs.get('location_id')
        locationComment = LocationComment.objects.filter(location_id=location_id)

        # location_id와 일치하는 데이터가 없을 경우 404 응답을 반환
        if not locationComment.exists():
            return Response({"detail": "Location comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 페이지네이션 적용
        paginator = CustomPageNumberPagination()
        paginated_comments = paginator.paginate_queryset(locationComment,request)
        serializer = LocationCommentSerializer(paginated_comments, many=True)

        return paginator.get_paginated_response(serializer.data)

# 고사장 리뷰 작성 [POST][/location/comment]
class createLocationComment(APIView):
    
    # 로그인한 사용자만 접근 가능
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request,*args, **kwargs):
        serializer = LocationCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 고사장 리뷰 수정 [PATCH][/location/comment]
class updateLocationComment(APIView):

    # 로그인한 사용자만 접근 가능
    permission_classes = [permissions.IsAuthenticated]

    # 게시물이 존재하는지 확인하는 메소드
    # 존재한다면 -> 해당 게시물 가져옴 / 존재하지 않는다면 -> None 반환
    # 메인 로직에서는 객체가 None인지만 확인하면 됨
    def get_object(self, user_id, location_id):
        try:
            return LocationComment.objects.get(user_id=user_id, location_id=location_id)
        except LocationComment.DoesNotExist:
            return None
        
    def patch(self, request, user_id, location_id, *args, **kwargs):
        comment = self.get_object(user_id,location_id)
        if comment is None:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 인증된 사용자와 게시물의 작성자가 동일한지 확인
        if request.user.id != UUID(user_id): #user_id가 string으로 오면 UUID로 변환
            return Response({"error":"Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LocationCommentSerializer(comment, data=request.data, partial=True) 
        # partial=True로 설정하여 부분 수정 가능
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

# 고사장 리뷰 삭제 [DELETE][/location/comment/]
class deleteLocationComment(APIView):
    
    # 로그인한 사용자만 접근 가능
    permission_classes = [permissions.IsAuthenticated]

    # 게시물이 존재하는지 확인하는 메소드
    def get_object(self, user_id, location_id):
        try:
            return LocationComment.objects.get(user_id=user_id, location_id=location_id)
        except LocationComment.DoesNotExist:
            return None

    def delete(self, request, user_id, location_id, *args, **kwargs):
        comment = self.get_object(user_id,location_id)
        if comment is None:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 인증된 사용자와 게시물의 작성자가 동일한지 확인
        if request.user.id != UUID(user_id): #user_id가 string으로 오면 UUID로 변환
            return Response({"error":"Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) # 삭제 성공

# 작성 고사장 리뷰 조회 [GET][/location/mycomment] 
class getMyComment(APIView):
    # 로그인한 사용자만 접근 가능
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        userID = request.user.id
        locationComment = LocationComment.objects.filter(user_id=userID)

        # userID와 일치하는 데이터가 없을 경우 404 응답을 반환
        if not locationComment.exists():
            return Response({"detail": "There is no comments from the user"}, status=status.HTTP_204_NO_CONTENT)
        
        # 페이지네이션 적용
        paginator = CustomPageNumberPagination()
        paginated_comments = paginator.paginate_queryset(locationComment,request)
        serializer = LocationCommentSerializer(paginated_comments, many=True)

        return paginator.get_paginated_response(serializer.data)

# 고사장 확인 [GET][/location]
class NearestLocation(APIView):
    permission_classes = [AllowAny]

    def get(self,request, *args, **kwargs):
        # 두 점 사이 거리
        def getDist(lon1, lat1, lon2,lat2):
            a = lon1 - lon2
            b = lat1 - lat2
            return a ** 2 + b ** 2
        
        # request_body에서 위도 경도 가져오기
        request_data = request.data
        lon = float(request_data.get('longitude'))
        lat = float(request_data.get('latitude'))
        
        # LocationInfo DB에서 address 필드만 가져오기 (모든 고사장에 대해서)
        all_exam_location = list(LocationInfo.objects.values('location_id','latitude', 'longitude'))
        
        # 고사장 거리 계산 후 반환된 결과값 저장할 리스트
        distances = []

        for location in all_exam_location:
            d = getDist(lon, lat, location['longitude'], location['latitude'])
            distances.append((location['location_id'], d))
            
        # 거리를 기준으로 오름차순 정렬 -> 상위 10개만 선택
        nearest10 = sorted(distances, key = lambda k: k[1])[:10]
        for i in nearest10:
            print(i)

        #JsonResponse로 반환
        response_data = []
        for item in nearest10:
            # location_id를 이용해 LocationInfo DB에서 해당 고사장의 모든 정보 가져오기
            location_instance = LocationInfo.objects.get(location_id=item[0])
            
            # 시리얼라이저로 JSON 형식 변환
            location_data = LocationInfoSerializer(location_instance).data
            location_data['distance'] = item[1]

            response_data.append(location_data)
            
        return Response(response_data, status=status.HTTP_200_OK)


'''
# 고사장 정보 DB에 넣기
class setLocationDB(APIView):
    permission_classes = [AllowAny]

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="
    endPoint = "http://openapi.q-net.or.kr/api/service/rest/InquiryExamAreaSVC/getList"

    def post(self, request, *args, **kwargs):
        naverEndPoint = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
        CLID = "0jvousuc1a"
        CLSC = "Fv681Ja00PiMfaSnpRSgkNdi2oXJ0PSqdymh8X0j"
        headers = {
            "X-NCP-APIGW-API-KEY-ID": CLID,
            "X-NCP-APIGW-API-KEY": CLSC
        }

        n = 2
        while n <= 2:
            if n <10:
                m = "0" + str(n)
            else:
                m = str(n)

            params = {"serviceKey": self.decodedKey,
                "brchCd": m,
                "numOfRows": 100,
                "pageNo": 1
                }
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            responseData = []
            i = 1
            for item in root.findall('.//item'):
                dict = {}
                dict["address"] = item.find('address').text

                db = LocationInfo.objects.filter(address=dict["address"])
                if len(db):
                    print("중복")
                    continue
                
                dict["brchNm"] = item.find('brchNm').text
                dict["examAreaGbNm"] = item.find('examAreaGbNm').text
                dict["examAreaNm"] = item.find('examAreaNm').text
                dict["plceLoctGid"] = item.find('plceLoctGid').text
                dict["telNo"] = item.find('telNo').text
                print('ok')
                if i <= 19:
                    i += 1
                    responseData.append(dict)
                    continue
                naverParams = {
                "query" : dict["address"], # 각 고사장 주소
                }
                response = requests.get(naverEndPoint, params=naverParams, headers=headers)
                data = json.loads(response.content)
                data = data["addresses"][0]
                dict["latitude"] = data["y"]
                dict["longtitude"] = data["x"]

                serializer = LocationInfoSerializer(data=dict)
                
                
                if serializer.is_valid():
                    serializer.save()
                    print("OK")
                    # return Response(status=status.HTTP_208_ALREADY_RE PORTED)
                else:
                    responseData.append(dict)
                    # return Response(status=status.HTTP_400_BAD_REQUEST)
            n += 1
        return Response(responseData, status=status.HTTP_201_CREATED)

class deleteLocationDB(APIView):
    permission_classes = [AllowAny] 

    def delete(self, request, *args, **kwargs):
        data = LocationInfo.objects.all()
        for item in data:
            item.delete()
            print('del')
        return Response(status=status.HTTP_205_RESET_CONTENT)
'''

# POST PATCH DELETE는 URL 동일 [location/comment/]
# 따라서 같은 클래스 내에 위치해야함
# 여러 HTTP 메소드를 한 클래스 내에서 다루기 위해 중앙 뷰 생성
class MainLocationCommentView(APIView) :
    
    # 로그인한 사용자만 접근 가능
    # 클래스 레벨에서 접근 권한 적용하기 위해 다시 작성
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return createLocationComment.as_view()(request, *args, **kwargs)
    
    def patch(self, request, user_id, location_id, *args, **kwargs):
        return updateLocationComment.as_view()(request, user_id, location_id, *args, **kwargs)
    
    def delete(self, request, user_id, location_id, *args, **kwargs):
        return deleteLocationComment.as_view()(request, user_id, location_id, *args, **kwargs)
