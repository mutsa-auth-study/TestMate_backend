from .models import Exam, ExamPlan, ExamFavorite, ExamRecent
from .serializers import ExamTotalSerializer, ExamDetailSerializer, ExamRecentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from django.shortcuts import get_list_or_404
import uuid

import xml.etree.ElementTree as ET
import requests

class ExamList(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        data = Exam.objects.all()
        exam_list = list(data.values())  # 시험 정보를 담을 리스트 초기화
        
        if request.user.is_authenticated:
            # 로그인한 사용자일 경우, 즐겨찾기한 시험 ID들을 가져와 리스트로 변환
            exam_favorites = ExamFavorite.objects.filter(user=request.user)
            favorite_exam_ids = [exam_favorite.exam_id for exam_favorite in exam_favorites]
    
            # 즐찾 여부 확인
            for exam in exam_list:
                if exam.exam_id in favorite_exam_ids:
                    exam["is_favorite"] = True
                else:
                    exam["is_favorite"] = False
            # 미로그인 사용자는 모두 즐찾X
        else:
            for exam in exam_list:
                exam["is_favorite"] = False

        # 시험들의 리스트 반환
        response_data = {
            "status": status.HTTP_200_OK,
            "information": exam_list
        }
        # status 예외처리는 어디서 어떻게 해주나..
        return Response(response_data, status=status.HTTP_200_OK)
      

# ExamFavorite 테이블에서 유저 id에 해당하는 시험 id 쭉 가져오고 해당 시험 id에 해당하는 시험정보를 is_favorite 속성을 다 True로 채운 후에 추가해서 응답할
class ExamFavoriteGet(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_id = request.user.id

        # 로그인한 사용자가 즐겨찾기한 시험 ID들 가져오기
        favorite_exam_ids = ExamFavorite.objects.filter(user_id=user_id).values_list('exam_id', flat=True)

        # 해당 시험 ID에 해당하는 시험 정보 전체 테이블에서 가져와서 리스트로 반환
        favorite_exams = Exam.objects.filter(id__in=favorite_exam_ids)

        exam_list = []
        for exam in favorite_exams:
            exam_data = ExamTotalSerializer(exam).data  # 시험 시리얼라이징

            # is_favorite 값을 모두 True로 설정
            exam_data['is_favorite'] = True

            exam_list.append(exam_data)

        return Response(exam_list, status=status.HTTP_200_OK)

# 즐겨찾기 시험 정보 등록(post)
class ExamFavoritePost(APIView):
    def post(self, request):
        user_id = request.user.id

        # 현재 즐겨찾기한 시험 ID 개수 확인
        favorite_count = ExamFavorite.objects.filter(user_id=user_id).count()

        # 즐겨찾기한 시험 개수가 5개 이상이면 실패 응답 반환
        if favorite_count >= 5:
            return Response({"detail": "You can only add up to 5 exams to favorites."}, status=status.HTTP_400_BAD_REQUEST)

        # 요청 데이터에서 즐겨찾기할 시험 ID 리스트 가져오기
        exam_ids = request.data.get('exam_ids', [])

        # 요청 데이터에 exam_ids가 없으면 실패 응답 반환
        if not exam_ids:
            return Response({"detail": "exam_ids are required."}, status=status.HTTP_400_BAD_REQUEST)

        added_exam_ids = []

        for exam_id in exam_ids:
            # 이미 즐겨찾기한 시험인지 확인 후 추가
            if not ExamFavorite.objects.filter(user_id=user_id, exam_id=exam_id).exists():
                added_exam_ids.append(exam_id)

        # 추가된 시험 ID 리스트를 응답으로 반환 => 맞나..?
        return Response({"information": [{"exam_id": exam_id} for exam_id in added_exam_ids]}, status=status.HTTP_201_CREATED)


# 즐겨찾기 시험 정보 삭제(delete)
# class ExamFavoriteDelete(APIView):






class ExamPlan(APIView):
    # def get(self, request, *args, **kwargs):
    #     # 예시: URL 파라미터에서 필터링 조건을 받아옴
    #     filter_param = request.GET.get('filter_param')

    #     if filter_param:
    #         queryset = YourModel.objects.filter(some_field=filter_param)
    #     else:
    #         queryset = YourModel.objects.all()

    #     serializer = YourModelSerializer(queryset, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = [AllowAny]

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="

    # 시험 일정
    endPoint = "http://apis.data.go.kr/B490007/qualExamSchd/getQualExamSchdList"

    def get(self, request, *args, **kwargs):
        def callAPI(qualgbCd, jmCd):
            # qualgbCd = request_data['qualgbCd']
            # jmCd = request_data['jmCd']
            params = {"serviceKey": self.decodedKey,
            "implYy": "2023",
            "qualgbCd": qualgbCd, #request
            "jmCd": jmCd, #request
            "numOfRows": "1", #임시
            "pageNo": "1",
            "dataFormat": "xml"
            }
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            dict = {}
            for item in root.findall('.//item'):
                dict["implYy"] = item.find('implYy').text
                dict["implSeq"] = item.find('implSeq').text
                # dict["exam_id"] = "exam_id"
                dict["description"] = item.find('description').text
                dict["docRegStartDt"] = item.find('docRegStartDt').text
                dict["docRegEndDt"] = item.find('docRegEndDt').text
                dict["docExamStartDt"] = item.find('docExamStartDt').text
                dict["docExamEndDt"] = item.find('docExamEndDt').text
                dict["docPassDt"] = item.find('docPassDt').text
                dict["pracRegStartDt"] = item.find('pracRegStartDt').text
                dict["pracRegEndDt"] = item.find('pracRegEndDt').text
                dict["pracExamStartDt"] = item.find('pracExamStartDt').text
                dict["pracExamEndDt"] = item.find('pracExamEndDt').text
                dict["pracPassDt"] = item.find('pracPassDt').text
            return dict

        request_data = request.data
        # additional_info = request.META.get('HTTP_X_ADDITIONAL_INFO', None)  # 예시로 요청 헤더에서 추가 정보를 가져옴
        examPlan = callAPI(request_data.get("qualgbCd"), request_data.get("jmCd"))
        # examPlan["exam_id"] = request_data["exam_id"]

        serializer = ExamDetailSerializer(data=examPlan)
        
        if serializer.is_valid():
            # serializer.save()  # 데이터베이스에 저장
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # 사용자가 시험을 조회했을 때, 그 정보 DB에 저장하는 로직
    # 이때, 개수를 체크하고 10개 초과 시 가장 오래된 정보 삭제

    def post(self, request):
        user_id = request.user.id
        exam_id = request.data.get('exam_id')

        # 새로운 조회 정보를 저장
        recent_exam = ExamRecent(user_id=user_id, exam_id=exam_id)
        recent_exam.save()

        # 현재 저장된 조회 정보의 개수 체크
        count = ExamRecent.objects.filter(user_id=user_id).count()

        # 10개 초과하는 경우 가장 오래된 정보 삭제
        if count > 10:
            oldest_exam = ExamRecent.objects.filter(user_id=user_id).earliest("recent_id")
            oldest_exam.delete()

        return Response({"message:": "Success"}, status=status.HTTP_201_CREATED)


# 최근조회 시험 조회 [GET] [exam/recent]
class RecentExamListView(APIView):
    # 인증
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # user_id를 인증된 사용자로부터 얻음
        user_id = request.user.id

        # 가장 최근 조회한 10개 정보 가져오기
        recent_exams = get_list_or_404(ExamRecent, user_id=user_id)[:10]

        # 시리얼라이저를 통해 JSON으로 변환
        serializer = ExamRecentSerializer(recent_exams, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


'''
# 호출은 되지만 xml 읽기에 실패하는듯. 아래에 파일 직접 읽어서 성공함.
class setExamDB(APIView):
    permission_classes = [AllowAny]

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG%2F%2B8nJcLHw%3D%3D"  # 발급받아야 함
    endPoint = "http://openapi.q-net.or.kr/api/service/rest/InquiryListNationalQualifcationSVC/getList"  # 요청 URL

    def post(self, request, *args, **kwargs):
        params = {"serviceKey": self.decodedKey}    # 
        response = requests.get(self.endPoint, params=params)
        root = ET.fromstring(response.content)
        
        for item in root.findall('.//item'):
            dict = {}
            dict["exam_id"] = uuid.uuid4() #시험id
            dict["jmcd"] = item.find('jmcd').text #종목코드
            dict["jmfldnm"] = item.find('jmfldnm').text #종목명
            dict["mdobligfldcd"] = item.find('mdobligfldcd').text #중직무분야코드
            dict["mdobligfldnm"]= item.find('mdobligfldnm').text #중직무분야명
            dict["obligfldcd"] = item.find('obligfldcd').text #대직무분야코드
            dict["obligfldnm"] = item.find('obligfldnm').text #대직무분야명
            dict["qualgbcd"] = item.find('qualgbcd').text #자격구분
            dict["qualgbnm"] = item.find('qualgbnm').text #자격구분명
            dict["seriescd"]= item.find('seriescd').text #계열코드
            dict["seriesnm"] = item.find('seriesnm').text #계열명
            serializer = ExamTotalSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
                print("OK")
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        return Response(status=status.HTTP_201_CREATED)

# 성공한 클래스
class setExamDB_XML(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        root = ET.parse('examList.xml')
        
        for item in root.findall('.//item'):
            dict = {}
            dict["exam_id"] = uuid.uuid4 #시험id
            dict["jmcd"] = item.find('jmcd').text #종목코드
            dict["jmfldnm"] = item.find('jmfldnm').text #종목명
            dict["qualgbcd"] = item.find('qualgbcd').text #자격구분
            dict["qualgbnm"] = item.find('qualgbnm').text #자격구분명
            dict["seriescd"]= item.find('seriescd').text #계열코드
            dict["seriesnm"] = item.find('seriesnm').text #계열명

            dict["mdobligfldcd"] = item.find('mdobligfldcd').text #중직무분야코드
            dict["mdobligfldnm"]= item.find('mdobligfldnm').text #중직무분야명
            dict["obligfldcd"] = item.find('obligfldcd').text #대직무분야코드
            dict["obligfldnm"] = item.find('obligfldnm').text #대직무분야명
            serializer = ExamTotalSerializer(data=dict)
            if serializer.is_valid():
                serializer.save()
                print("OK")
            else:
                print("not")
            
            
            
        return Response(status=status.HTTP_201_CREATED)
   

class deleteExamDB_XML(APIView):
    permission_classes = [AllowAny] 

    def delete(self, request, *args, **kwargs):
        root = ET.parse('examList.xml')
        
        for item in root.findall('.//item'):
            data = Exam.objects.filter(jmcd = item.find('jmcd').text)
            for i in data:
                i.delete()
                print("del")
            
        # return Response(status=status.HTTP_201_CREATED)
'''