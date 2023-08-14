from rest_framework import generics
from rest_framework import mixins

from .models import Exam, ExamPlan, ExamFavorite
from .serializers import ExamTotalSerializer, ExamDetailSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import uuid

import xml.etree.ElementTree as ET
import requests
'''
class ExamTotalAPIMixins(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamTotalSerializer
    # GET 메소드 처리 (전체목록)
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class ExamDetailAPIMixins(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = ExamPlan.objects.all()
    serializer_class = ExamDetailSerializer
    lookup_field = 'exam_id'
    
    # GET 메소드 처리 (시험ID에 해당하는 1개의 시험 일정 불러옴)
    def get(self, request,*args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    '''
# 시험 정보 전체를 DB에 넣는 class => 이것도 /exam/
class setExamDB(APIView):
    permission_classes = [AllowAny]

    decodedKey = "YOUR_DECODED_SERVICE_KEY"  # 발급받아야 함
    endPoint = "YOUR_API_ENDPOINT_URL"  # 요청 URL

    def get(self, request, *args, **kwargs):

        def callAPI():  # 파라미터 없음..
            params = {"serviceKey": self.decodedKey}    # 
            response = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            
            dict = {}
            for item in root.findall('.//item'):
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
            
            return dict
        
        request_data = request.data
        # 필요한 데이터를 직렬화해서 데이터베이스에 저장하는 등의 처리를 여기서 진행
        Exam = callAPI()
        Exam["exam_id"] = request_data["exam_id"]

        serializer = ExamTotalSerializer(data=Exam)
        if serializer.is_valid():
            serializer.save()   # 데이터 베이스에 저장
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 시험 전체 목록을 제공하는 API + 로그인 시 각 시험의 즐겨찾기 여부도 제공
class ExamInfoView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, some_exam_id): # exam_id는 프론트에서 다 넘겨줘야할 듯..? => is_favorite을 채우려면
        exam = Exam.objects.get(pk=some_exam_id)  # 해당 exam_id의 특정 Exam 객체를 가져옴 => some_exam_id
        # user_id = request.data.get('user_id')
        if request.user.is_authenticated:
            # 로그인한 사용자
            # ExamFavorite 모델에서 user_id와 exam_id 확인하여 즐겨찾기 여부를 판단
            is_favorite = ExamFavorite.objects.filter(user=request.user, exam_id=some_exam_id).exists()
        else:
            # 로그인하지 않은 사용자
            is_favorite = None

        serializer = ExamTotalSerializer(exam)  # Exam 객체를 시리얼라이징
        exam_data = serializer.data  # 시리얼라이즈된 데이터 가져오기
        exam_data['is_favorite'] = is_favorite # 위에서 조건문 처리한 is_favorite을 exam_data에 추가로 넣어줌

        return response(exam_data, status=status.HTTP_200_OK)

# 내가 이해한 바로는 로그인한 사용자가 ExamFavorite 테이블에서 유저 id에 해당하는 시험 id 쭉 가져오고 해당 시험 id에 해당하는거만 시험 전체 테이블에서 뽑아서 반환?

class ExamFavoriteView(APIView):

    def get(self, request):
        user_id = request.user.id

        # 로그인한 사용자가 즐겨찾기한 시험 ID들 가져오기
        favorite_exam_ids = ExamFavorite.objects.filter(user_id=user_id).values_list('exam_id', flat=True)

        # 해당 시험 ID에 해당하는 시험 정보 전체 테이블에서 뽑아서 응답
        favorite_exams = Exam.objects.filter(id__in=favorite_exam_ids)
        # serializer = ExamTotalSerializer(favorite_exams, many=True)

        # 응답 형식에 맞게 구성
        response_data = {
            "check": True,
            "information": [{"exam_id": exam.id} for exam in favorite_exams]
        }

        return response(response_data, status=status.HTTP_200_OK)

class ExamDetail(APIView):
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
    
