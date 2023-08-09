from rest_framework import generics
from rest_framework import mixins

from .models import Exam, ExamPlan
from .serializers import ExamTotalSerializer, ExamDetailSerializer

from rest_framework.views import APIView
from rest_framework import response, status
import xml.etree.ElementTree as ET
import requests

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
    
# 공공데이터 호출, post까지 하는 시험 일정 조회 API

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

    decodedKey = "WKylCY9PiFAjyG1rstW8XGqQbs7lkyQWXRGIpZDC5RNJnSdK9W0BaUJF5KPRI6Y2e2VsiB9loeLTG/+8nJcLHw=="

    # 시험 일정
    endPoint = "http://apis.data.go.kr/B490007/qualExamSchd/getQualExamSchdList"

    def get(self, request, *args, **kwargs):
        def callAPI(qualgbCd, jmCd):
            qualgbCd = request_data['qualgbCd']
            jmCd = request_data['jmCd']
            params = {"serviceKey": self.decodedKey,
            "implYy": "2023",
            "qualgbCd": qualgbCd, #request
            "jmCd": jmCd, #request
            "numOfRows": "1", #임시
            "pageNo": "1",
            "dataFormat": "xml"
            }
            esponse = requests.get(self.endPoint, params=params)
            root = ET.fromstring(response.content)
            dict = {}
            for item in root.findall('.//item'):
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
        examPlan = callAPI(request_data["qualgbCd"], request_data["jmCd"])
        examPlan["exam_id"] = request_data["exam_id"]

        serializer = ExamDetailSerializer(data=examPlan)
        
        if serializer.is_valid():
            serializer.save()  # 데이터베이스에 저장
            return response(serializer.data, status=status.HTTP_201_CREATED)
        
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
